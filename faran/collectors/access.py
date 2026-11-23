from typing import Final, Sequence

from faran.types import (
    SimulationDataAccessor,
    StateSequence,
    Control,
    Risk,
    ObstacleStates,
    StateTrajectories,
)


class access:
    """Namespace of typed accessors for retrieving simulation data by key.

    Attributes:
        states: Initial state of each planning step.
        controls: Control output of each planning step.
        risks: Risk values of each evaluation.
        trajectories: Rollout state trajectories of each planning step.
        obstacle_states: Obstacle states before observation.
        obstacle_observations: Observed obstacle states.
        obstacle_forecasts: Predicted obstacle states of each planning step.
    """

    states: Final = SimulationDataAccessor.create(StateSequence, key="states")
    controls: Final = SimulationDataAccessor.create(Sequence[Control], key="controls")
    risks: Final = SimulationDataAccessor.create(Sequence[Risk], key="risks")
    trajectories: Final = SimulationDataAccessor.create(
        Sequence[StateTrajectories], key="trajectories"
    )
    obstacle_states: Final = SimulationDataAccessor.create(
        ObstacleStates, key="obstacle_states"
    )
    obstacle_observations: Final = SimulationDataAccessor.create(
        ObstacleStates, key="obstacle_observations"
    )
    obstacle_forecasts: Final = SimulationDataAccessor.create(
        Sequence[ObstacleStates], key="obstacle_forecasts"
    )
