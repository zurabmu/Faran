from typing import cast, Any
from dataclasses import dataclass

from faran.types import (
    jaxtyped,
    pytree,
    Array,
    DataType,
    JaxState,
    JaxStateBatch,
    JaxControlInputSequence,
    JaxControlInputBatch,
    JaxDynamicalModel,
    JaxCostFunction,
    JaxSampler,
    JaxUpdateFunction,
    JaxPaddingFunction,
    JaxFilterFunction,
    Mppi,
    DebugData,
    Control,
)
from faran.mppi.common import UseOptimalControlUpdate, NoFilter
from faran.mppi.compilation import compiled

from jaxtyping import Array as JaxArray, Float, Scalar

import jax
import jax.numpy as jnp
import numpy as np


@jaxtyped
@pytree
@dataclass(frozen=True)
class JaxWeights:
    """Softmax-normalized cost weights used to compute the weighted average over rollouts."""

    _array: Float[JaxArray, " M"]

    def __array__(self, dtype: DataType | None = None) -> Float[Array, " M"]:
        return np.asarray(self._array)

    @property
    def rollout_count(self) -> int:
        return self._array.shape[0]

    @property
    def array(self) -> Float[JaxArray, " M"]:
        return self._array


class JaxZeroPadding(
    JaxPaddingFunction[JaxControlInputSequence, JaxControlInputSequence]
):
    """Fills shifted-out time steps with zero control inputs after horizon advancement."""

    def __call__(
        self, *, nominal_input: JaxControlInputSequence, padding_size: int
    ) -> JaxControlInputSequence:
        padding_array = jnp.zeros((padding_size, nominal_input.array.shape[1]))
        return nominal_input.similar(array=padding_array)


@dataclass(kw_only=True, frozen=True)
class JaxMppi[
    StateT: JaxState,
    StateBatchT: JaxStateBatch,
    ControlInputSequenceT: JaxControlInputSequence,
    ControlInputBatchT: JaxControlInputBatch,
    ControlInputPaddingT: JaxControlInputSequence = ControlInputSequenceT,
](Mppi[StateT, ControlInputSequenceT, JaxWeights]):
    """Sampling-based stochastic optimal controller using the information-theoretic MPPI algorithm."""

    planning_interval: int
    model: JaxDynamicalModel[
        StateT, Any, StateBatchT, ControlInputSequenceT, ControlInputBatchT
    ]
    cost_function: JaxCostFunction
    sampler: JaxSampler[ControlInputSequenceT, ControlInputBatchT]
    update_function: JaxUpdateFunction[ControlInputSequenceT]
    padding_function: JaxPaddingFunction[ControlInputSequenceT, ControlInputPaddingT]
    filter_function: JaxFilterFunction[ControlInputSequenceT]

    @staticmethod
    def create[
        S: JaxState,
        SB: JaxStateBatch,
        CIS: JaxControlInputSequence,
        CIB: JaxControlInputBatch,
        CIP: JaxControlInputSequence = CIS,
    ](
        *,
        planning_interval: int = 1,
        model: JaxDynamicalModel[S, Any, SB, CIS, CIB],
        cost_function: JaxCostFunction,
        sampler: JaxSampler[CIS, CIB],
        update_function: JaxUpdateFunction[CIS] | None = None,
        padding_function: JaxPaddingFunction[CIS, CIP] | None = None,
        filter_function: JaxFilterFunction[CIS] | None = None,
    ) -> "JaxMppi[S, SB, CIS, CIB, CIP]":
        """Creates an MPPI planner.

        Args:
            model: Simulates each rollout.
            cost_function: Scores each rollout at each time step.
            sampler: Draws the control perturbations of the rollouts.
            planning_interval: Number of time steps that the nominal sequence is
                shifted by after each planner step. Must be positive.
            update_function: Computes the next nominal sequence from the optimal
                one. Without one, the optimal sequence becomes the nominal sequence.
            padding_function: Fills the time steps at the end of the shifted nominal
                sequence. Without one, they are filled with zeros.
            filter_function: Smooths the optimal sequence, for example a
                Savitzky-Golay filter. Without one, it is not filtered.
        """
        return JaxMppi(
            planning_interval=planning_interval,
            model=model,
            cost_function=cost_function,
            sampler=sampler,
            update_function=update_function
            or cast(JaxUpdateFunction[CIS], UseOptimalControlUpdate()),
            padding_function=padding_function
            or cast(JaxPaddingFunction[CIS, CIP], JaxZeroPadding()),
            filter_function=filter_function or cast(JaxFilterFunction[CIS], NoFilter()),
        )

    def __post_init__(self) -> None:
        assert self.planning_interval > 0, "Planning interval must be positive."

    def step(
        self,
        *,
        temperature: float,
        nominal_input: ControlInputSequenceT,
        initial_state: StateT,
    ) -> Control[ControlInputSequenceT, JaxWeights]:
        """Samples rollouts, evaluates costs, and returns the cost-weighted optimal control."""
        assert temperature > 0.0, "Temperature must be positive."

        return step(
            self,
            temperature=jnp.asarray(temperature),
            nominal_input=nominal_input,
            initial_state=initial_state,
        )


@compiled
def step[
    StateT: JaxState,
    ControlInputSequenceT: JaxControlInputSequence,
](
    planner: JaxMppi[StateT, Any, ControlInputSequenceT, Any, Any],
    *,
    temperature: Scalar,
    nominal_input: ControlInputSequenceT,
    initial_state: StateT,
) -> Control[ControlInputSequenceT, JaxWeights]:
    samples = planner.sampler.sample(around=nominal_input)

    rollouts = planner.model.simulate(inputs=samples, initial_state=initial_state)
    costs = planner.cost_function(inputs=samples, states=rollouts)

    optimal_control, weights = compute_weighted_control(
        samples.array, costs.array, temperature
    )
    optimal_input = planner.filter_function(
        optimal_input=nominal_input.similar(array=optimal_control)
    )

    nominal_input = planner.update_function(
        nominal_input=nominal_input, optimal_input=optimal_input
    )

    shifted_control = shift_control_left(
        nominal_input.array,
        padding_array=planner.padding_function(
            nominal_input=nominal_input, padding_size=planner.planning_interval
        ).array,
        planning_interval=planner.planning_interval,
    )

    return Control(
        optimal=optimal_input,
        nominal=nominal_input.similar(array=shifted_control),
        debug=DebugData(trajectory_weights=JaxWeights(weights)),
    )


@jax.jit
@jaxtyped
def compute_weighted_control(
    samples: Float[JaxArray, "T D_u M"],
    costs: Float[JaxArray, "T M"],
    temperature: Scalar,
) -> tuple[Float[JaxArray, "T D_u"], Float[JaxArray, " M"]]:
    total_costs = jnp.sum(costs, axis=0)
    min_cost = jnp.min(total_costs)
    exp_costs = jnp.exp((total_costs - min_cost) / (-temperature))
    normalizing_constant = jnp.sum(exp_costs)
    weights = exp_costs / normalizing_constant

    return jnp.tensordot(samples, weights, axes=([2], [0])), weights


@jax.jit(static_argnames=("planning_interval",))
@jaxtyped
def shift_control_left(
    control: Float[JaxArray, "T D_u"],
    *,
    padding_array: Float[JaxArray, "P D_u"],
    planning_interval: int,
) -> Float[JaxArray, "T D_u"]:
    return jnp.concatenate([control[planning_interval:], padding_array], axis=0)
