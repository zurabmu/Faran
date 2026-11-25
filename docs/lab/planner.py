from typing import Protocol

import numpy as np
from numpy.typing import ArrayLike

from faran import Mppi
from faran.numpy import costs, extract, filters, model, mppi, sampler, types

from .config import CONFIG
from .scene import Reference

type AugmentedState = types.augmented.State[types.bicycle.State, types.simple.State]
type AugmentedInputs = types.augmented.ControlInputSequence[
    types.bicycle.ControlInputSequence, types.simple.ControlInputSequence
]
type Planner = Mppi[AugmentedState, AugmentedInputs]


class Dynamics(Protocol):
    def step(self, inputs: AugmentedInputs, state: AugmentedState) -> AugmentedState:
        """Returns the state one time step after `state`, under the first input."""
        ...

    def forward(self, inputs: AugmentedInputs, state: AugmentedState) -> ArrayLike:
        """Returns the states that `inputs` lead to from `state`."""
        ...


def mpcc_planner(
    *,
    reference: Reference,
    rollout_count: int,
    cost_terms: tuple[types.CostFunction, ...],
    minimum_progress_speed: float,
) -> tuple[Planner, Dynamics]:
    """An MPCC planner for the bicycle model, and the model it plans with."""
    planner, augmented_model, _, _ = mppi.mpcc(
        model=bicycle_model(),
        sampler=bicycle_sampler(rollout_count=rollout_count),
        costs=cost_terms,
        reference=reference,
        position_extractor=position_extractor(),
        config={
            "weights": {"contouring": 50.0, "lag": 100.0, "progress": 1000.0},
            "virtual": {"velocity_limits": (minimum_progress_speed, 15.0)},
        },
        filter_function=filters.savgol(window_length=11, polynomial_order=3),  # pyright: ignore[reportArgumentType]
    )
    return planner, augmented_model


def vehicle_positions(states: types.bicycle.StateBatch) -> types.bicycle.Positions:
    return states.positions


def vehicle_headings(states: types.bicycle.StateBatch) -> types.Headings:
    return types.headings(heading=states.heading())


def position_extractor():
    return extract.from_physical(vehicle_positions)


def control_smoothing():
    return costs.comfort.control_smoothing(weights=np.array([5.0, 20.0, 5.0]))


def bicycle_model():
    return model.bicycle.dynamical(
        time_step_size=CONFIG.time_step,
        wheelbase=CONFIG.wheelbase,
        speed_limits=(0.0, 15.0),
        steering_limits=(-0.5, 0.5),
        acceleration_limits=(-3.0, 3.0),
    )


def bicycle_sampler(*, rollout_count: int):
    return sampler.gaussian(
        standard_deviation=[0.5, 0.2],
        rollout_count=rollout_count,
        to_batch=types.bicycle.control_input_batch.create,
        seed=42,
    )
