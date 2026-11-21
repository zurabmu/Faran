from typing import Sequence
from dataclasses import dataclass

from faran import Control, DataType, DebugData
from faran_visualizer import Array, JaxArray, MpccSimulationResult
from tests.dsl.backends import Backend, States

from jaxtyping import Float

import numpy as np


@dataclass(frozen=True)
class StubRisk:
    """Placeholder for the risk of each rollout over the horizon."""

    values: Float[Array, "T M"] | Float[JaxArray, "T M"]

    def __array__(self, dtype: DataType | None = None) -> Float[Array, "T M"]:
        return np.asarray(self.values, dtype=dtype)

    @property
    def horizon(self) -> int:
        return self.values.shape[0]

    @property
    def rollout_count(self) -> int:
        return self.values.shape[1]


@dataclass(frozen=True)
class StubWeights:
    """Placeholder for the trajectory weights a planner computes for its rollouts."""

    values: Float[Array, " M"] | Float[JaxArray, " M"]

    def __array__(self, dtype: DataType | None = None) -> Float[Array, " M"]:
        return np.asarray(self.values, dtype=dtype)

    @property
    def rollout_count(self) -> int:
        return self.values.shape[0]


@dataclass(frozen=True)
class MpccData:
    """Builds MPCC simulation results with the arrays of one backend."""

    backend: Backend

    def states(
        self,
        *,
        x: Sequence[float],
        path_parameters: Sequence[float] | None = None,
    ) -> States:
        count = len(x)
        physical = np.zeros((count, 4))
        physical[:, 0] = x
        virtual = (
            np.zeros((count, 1))
            if path_parameters is None
            else np.array(path_parameters, dtype=float).reshape(-1, 1)
        )
        return self.backend.states(physical=physical, virtual=virtual)

    def control(self, *, weights: Sequence[float]) -> Control:
        no_inputs = self.backend.no_inputs()
        return Control(
            optimal=no_inputs,
            nominal=no_inputs,
            debug=DebugData(
                trajectory_weights=StubWeights(self.backend.array(weights))
            ),
        )

    def risk(self, values: Sequence[Sequence[float]]) -> StubRisk:
        """Creates the risk of each rollout (columns) over the horizon (rows)."""
        return StubRisk(self.backend.array(values))

    def result(
        self,
        *,
        states: States | None = None,
        path_length: float = 10.0,
        contouring_errors: Sequence[float] | None = None,
        lag_errors: Sequence[float] | None = None,
        max_contouring_error: float | None = None,
        max_lag_error: float | None = None,
        risks: Sequence[StubRisk] | None = None,
        controls: Sequence[Control] | None = None,
    ) -> MpccSimulationResult:
        states = states if states is not None else self.states(x=[0.0, 1.0])
        step_count = len(np.asarray(states.virtual))
        return MpccSimulationResult(
            reference=self.backend.reference(path_length=path_length),
            states=states,
            contouring_errors=self.backend.array(
                contouring_errors
                if contouring_errors is not None
                else np.zeros(step_count)
            ),
            lag_errors=self.backend.array(
                lag_errors if lag_errors is not None else np.zeros(step_count)
            ),
            time_step_size=0.1,
            wheelbase=2.0,
            vehicle_width=1.0,
            max_contouring_error=max_contouring_error,
            max_lag_error=max_lag_error,
            risks=risks,
            controls=controls,
        )
