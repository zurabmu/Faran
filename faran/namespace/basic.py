from typing import Final, Any

from faran.types import (
    NumPyState,
    NumPyStateSequence,
    NumPyStateBatch,
    NumPyControlInputSequence,
    NumPyControlInputBatch,
    NumPyCosts,
    NumPyCostFunction,
    State as State,
    StateSequence as StateSequence,
    StateBatch as StateBatch,
    ControlInputSequence as ControlInputSequence,
    ControlInputBatch as ControlInputBatch,
    Costs as Costs,
    CostFunction as CostFunction,
    NumPyPathParameters,
    NumPyReferencePoints,
    NumPyPositions,
    NumPySimplePositions,
    NumPyHeadings,
    NumPyLateralPositions,
    NumPyLongitudinalPositions,
    NumPyNormals,
    NumPyRisk,
    NumPyPathParameterExtractor,
    NumPyPathVelocityExtractor,
    NumPyPositionExtractor,
    NumPyDistanceExtractor,
    NumPyRiskMetric,
    Error as Error,  # NOTE: Aliased to workaround ruff bug.
    Risk as Risk,
    RiskMetric as RiskMetric,
    ContouringCost as ContouringCost,
    NumPySampledObstacleStates,
    NumPySampledObstaclePositions,
    NumPySampledObstacleHeadings,
    NumPySampledObstaclePositionExtractor,
    NumPySampledObstacleHeadingExtractor,
    NumPyObstacleStates,
    NumPyObstacleStatesForTimeStep,
    NumPyObstacleStateProvider,
    NumPyObstaclePositionExtractor,
    NumPyBoundaryDistance,
    NumPyBoundaryDistanceExtractor,
)
from faran.mppi import NumPyWeights
from faran.models import (
    NumPyBicycleState,
    NumPyBicycleStateSequence,
    NumPyBicycleStateBatch,
    NumPyBicyclePositions,
    NumPyBicycleControlInputSequence,
    NumPyBicycleControlInputBatch,
    NumPyBicycleObstacleStates,
    NumPyBicycleObstacleInputs,
    NumPyBicycleObstacleStateSequences,
    NumPyIntegratorObstacleStateSequences,
    NumPyUnicycleState,
    NumPyUnicycleStateSequence,
    NumPyUnicycleStateBatch,
    NumPyUnicyclePositions,
    NumPyUnicycleControlInputSequence,
    NumPyUnicycleControlInputBatch,
    NumPyUnicycleObstacleStates,
    NumPyUnicycleObstacleInputs,
    NumPyUnicycleObstacleStateSequences,
)
from faran.costs import (
    NumPyPreference,
    NumPyContouringCost,
    NumPyDistance,
)
from faran.obstacles import (
    NumPyObstacleIds,
    NumPySampledObstacle2dPoses,
    NumPyObstacle2dPoses,
    NumPyObstacle2dPosesForTimeStep,
    NumPyObstacle2dPositions,
    NumPyObstacle2dPositionsForTimeStep,
    NumPyObstacleHeadings,
    NumPyObstacleHeadingsForTimeStep,
    NumPyObstacleStatesRunningHistory,
)
from faran.states import (
    NumPySimpleState,
    NumPySimpleStateSequence,
    NumPySimpleStateBatch,
    NumPySimpleControlInputSequence,
    NumPySimpleControlInputBatch,
    NumPySimpleCosts,
    NumPySimpleSampledObstacleStates,
    NumPySimpleObstacleStatesForTimeStep,
    NumPySimpleObstacleStates,
    NumPyAugmentedState,
    NumPyAugmentedStateSequence,
    NumPyAugmentedStateBatch,
    NumPyAugmentedControlInputSequence,
    NumPyAugmentedControlInputBatch,
)


class types:
    type State = NumPyState
    type StateSequence = NumPyStateSequence
    type StateBatch = NumPyStateBatch
    type ControlInputSequence = NumPyControlInputSequence
    type ControlInputBatch = NumPyControlInputBatch
    type Costs = NumPyCosts
    type PathParameters = NumPyPathParameters
    type ReferencePoints = NumPyReferencePoints
    type Positions = NumPyPositions
    type Headings = NumPyHeadings
    type LateralPositions = NumPyLateralPositions
    type LongitudinalPositions = NumPyLongitudinalPositions
    type ObstacleIds = NumPyObstacleIds
    type SampledObstacleStates = NumPySampledObstacleStates
    type SampledObstaclePositions = NumPySampledObstaclePositions
    type SampledObstacleHeadings = NumPySampledObstacleHeadings
    type SampledObstaclePositionExtractor[SampledStatesT] = (
        NumPySampledObstaclePositionExtractor[SampledStatesT]
    )
    type SampledObstacleHeadingExtractor[SampledStatesT] = (
        NumPySampledObstacleHeadingExtractor[SampledStatesT]
    )
    type ObstacleStates[SingleSampleT = Any, ObstacleStatesForTimeStepT = Any] = (
        NumPyObstacleStates[SingleSampleT, ObstacleStatesForTimeStepT]
    )
    type ObstacleStatesForTimeStep[ObstacleStatesT = Any] = (
        NumPyObstacleStatesForTimeStep[ObstacleStatesT]
    )
    type ObstaclePositionExtractor[
        ObstacleStatesForTimeStepT,
        ObstacleStatesT,
        PositionsForTimeStepT,
        PositionsT,
    ] = NumPyObstaclePositionExtractor[
        ObstacleStatesForTimeStepT,
        ObstacleStatesT,
        PositionsForTimeStepT,
        PositionsT,
    ]
    type SampledObstacle2dPoses = NumPySampledObstacle2dPoses
    type Obstacle2dPoses = NumPyObstacle2dPoses
    type Obstacle2dPosesForTimeStep = NumPyObstacle2dPosesForTimeStep
    type Obstacle2dPositions = NumPyObstacle2dPositions
    type Obstacle2dPositionsForTimeStep = NumPyObstacle2dPositionsForTimeStep
    type ObstacleHeadings = NumPyObstacleHeadings
    type ObstacleHeadingsForTimeStep = NumPyObstacleHeadingsForTimeStep
    type ObstacleStatesRunningHistory[
        StatesT,
        StatesForTimeStepT: NumPyObstacleStatesForTimeStep,
    ] = NumPyObstacleStatesRunningHistory[StatesT, StatesForTimeStepT]
    type Distance = NumPyDistance
    type BoundaryDistance = NumPyBoundaryDistance
    type Risk = NumPyRisk
    type Preference = NumPyPreference

    type Weights = NumPyWeights
    type CostFunction = NumPyCostFunction
    type PathParameterExtractor[StateBatchT] = NumPyPathParameterExtractor[StateBatchT]
    type PathVelocityExtractor[InputBatchT] = NumPyPathVelocityExtractor[InputBatchT]
    type PositionExtractor[StateBatchT] = NumPyPositionExtractor[StateBatchT]
    type DistanceExtractor[StateBatchT, SampledObstacleStatesT, DistanceT] = (
        NumPyDistanceExtractor[StateBatchT, SampledObstacleStatesT, DistanceT]
    )
    type BoundaryDistanceExtractor[StateBatchT, DistanceT] = (
        NumPyBoundaryDistanceExtractor[StateBatchT, DistanceT]
    )
    type RiskMetric[StateBatchT, ObstacleStatesT, SampledObstacleStatesT] = (
        NumPyRiskMetric[StateBatchT, ObstacleStatesT, SampledObstacleStatesT]
    )
    type ContouringCost[StateBatchT] = NumPyContouringCost[StateBatchT]
    type ObstacleStateProvider[ObstacleStatesT] = NumPyObstacleStateProvider[
        ObstacleStatesT
    ]

    path_parameters: Final = NumPyPathParameters
    reference_points: Final = NumPyReferencePoints.create
    positions: Final = NumPySimplePositions.create
    headings: Final = NumPyHeadings.create
    lateral_positions: Final = NumPyLateralPositions.create
    longitudinal_positions: Final = NumPyLongitudinalPositions.create
    normals: Final = NumPyNormals.create
    distance: Final = NumPyDistance
    boundary_distance: Final = NumPyBoundaryDistance
    preference: Final = NumPyPreference.create
    obstacle_ids: Final = NumPyObstacleIds
    obstacle_2d_poses: Final = NumPyObstacle2dPoses
    obstacle_2d_poses_for_time_step: Final = NumPyObstacle2dPosesForTimeStep
    obstacle_states_running_history: Final = NumPyObstacleStatesRunningHistory

    class simple:
        type State = NumPySimpleState
        type StateSequence = NumPySimpleStateSequence
        type StateBatch = NumPySimpleStateBatch
        type ControlInputSequence = NumPySimpleControlInputSequence
        type ControlInputBatch = NumPySimpleControlInputBatch
        type Costs = NumPySimpleCosts
        type SampledObstacleStates = NumPySimpleSampledObstacleStates
        type ObstacleStatesForTimeStep = NumPySimpleObstacleStatesForTimeStep
        type ObstacleStates = NumPySimpleObstacleStates

        state: Final = NumPySimpleState
        state_sequence: Final = NumPySimpleStateSequence
        state_batch: Final = NumPySimpleStateBatch
        control_input_sequence: Final = NumPySimpleControlInputSequence
        control_input_batch: Final = NumPySimpleControlInputBatch
        costs: Final = NumPySimpleCosts
        obstacle_states: Final = NumPySimpleObstacleStates
        obstacle_states_for_time_step: Final = NumPySimpleObstacleStatesForTimeStep

    class integrator:
        type ObstacleStateSequences = NumPyIntegratorObstacleStateSequences

    class bicycle:
        type State = NumPyBicycleState
        type StateSequence = NumPyBicycleStateSequence
        type StateBatch = NumPyBicycleStateBatch
        type Positions = NumPyBicyclePositions
        type ControlInputSequence = NumPyBicycleControlInputSequence
        type ControlInputBatch = NumPyBicycleControlInputBatch
        type ObstacleStates = NumPyBicycleObstacleStates
        type ObstacleInputs = NumPyBicycleObstacleInputs
        type ObstacleStateSequences = NumPyBicycleObstacleStateSequences

        state: Final = NumPyBicycleState
        state_sequence: Final = NumPyBicycleStateSequence
        state_batch: Final = NumPyBicycleStateBatch
        positions: Final = NumPyBicyclePositions
        control_input_sequence: Final = NumPyBicycleControlInputSequence
        control_input_batch: Final = NumPyBicycleControlInputBatch
        obstacle_states: Final = NumPyBicycleObstacleStates
        obstacle_inputs: Final = NumPyBicycleObstacleInputs
        obstacle_state_sequences: Final = NumPyBicycleObstacleStateSequences

    class unicycle:
        type State = NumPyUnicycleState
        type StateSequence = NumPyUnicycleStateSequence
        type StateBatch = NumPyUnicycleStateBatch
        type Positions = NumPyUnicyclePositions
        type ControlInputSequence = NumPyUnicycleControlInputSequence
        type ControlInputBatch = NumPyUnicycleControlInputBatch
        type ObstacleStates = NumPyUnicycleObstacleStates
        type ObstacleInputs = NumPyUnicycleObstacleInputs
        type ObstacleStateSequences = NumPyUnicycleObstacleStateSequences

        state: Final = NumPyUnicycleState
        state_sequence: Final = NumPyUnicycleStateSequence
        state_batch: Final = NumPyUnicycleStateBatch
        positions: Final = NumPyUnicyclePositions
        control_input_sequence: Final = NumPyUnicycleControlInputSequence
        control_input_batch: Final = NumPyUnicycleControlInputBatch
        obstacle_states: Final = NumPyUnicycleObstacleStates
        obstacle_inputs: Final = NumPyUnicycleObstacleInputs
        obstacle_state_sequences: Final = NumPyUnicycleObstacleStateSequences

    class augmented:
        type State[P: NumPyState, V: NumPyState] = NumPyAugmentedState[P, V]
        type StateSequence[P: NumPyStateSequence, V: NumPyStateSequence] = (
            NumPyAugmentedStateSequence[P, V]
        )
        type StateBatch[P: NumPyStateBatch, V: NumPyStateBatch] = (
            NumPyAugmentedStateBatch[P, V]
        )
        type ControlInputSequence[
            P: NumPyControlInputSequence,
            V: NumPyControlInputSequence,
        ] = NumPyAugmentedControlInputSequence[P, V]
        type ControlInputBatch[
            P: NumPyControlInputBatch,
            V: NumPyControlInputBatch,
        ] = NumPyAugmentedControlInputBatch[P, V]

        state: Final = NumPyAugmentedState
        state_sequence: Final = NumPyAugmentedStateSequence
        state_batch: Final = NumPyAugmentedStateBatch
        control_input_sequence: Final = NumPyAugmentedControlInputSequence
        control_input_batch: Final = NumPyAugmentedControlInputBatch


class classes:
    State: Final = NumPyState
    StateSequence: Final = NumPyStateSequence
    StateBatch: Final = NumPyStateBatch
    ControlInputSequence: Final = NumPyControlInputSequence
    ControlInputBatch: Final = NumPyControlInputBatch
    Costs: Final = NumPyCosts
    PathParameters: Final = NumPyPathParameters
    ReferencePoints: Final = NumPyReferencePoints
    Positions: Final = NumPyPositions
    Headings: Final = NumPyHeadings
    LateralPositions: Final = NumPyLateralPositions
    LongitudinalPositions: Final = NumPyLongitudinalPositions
    ObstacleIds: Final = NumPyObstacleIds
    ObstacleStates: Final = NumPyObstacleStates
    ObstacleStatesForTimeStep: Final = NumPyObstacleStatesForTimeStep
    SampledObstacleStates: Final = NumPySampledObstacleStates
    SampledObstaclePositions: Final = NumPySampledObstaclePositions
    SampledObstacleHeadings: Final = NumPySampledObstacleHeadings
    SampledObstaclePositionExtractor: Final = NumPySampledObstaclePositionExtractor
    SampledObstacleHeadingExtractor: Final = NumPySampledObstacleHeadingExtractor
    SampledObstacle2dPoses: Final = NumPySampledObstacle2dPoses
    Obstacle2dPoses: Final = NumPyObstacle2dPoses
    Obstacle2dPosesForTimeStep: Final = NumPyObstacle2dPosesForTimeStep
    Obstacle2dPositions: Final = NumPyObstacle2dPositions
    Obstacle2dPositionsForTimeStep: Final = NumPyObstacle2dPositionsForTimeStep
    ObstacleHeadings: Final = NumPyObstacleHeadings
    ObstacleHeadingsForTimeStep: Final = NumPyObstacleHeadingsForTimeStep
    ObstacleStatesRunningHistory: Final = NumPyObstacleStatesRunningHistory
    ObstaclePositionExtractor: Final = NumPyObstaclePositionExtractor
    Distance: Final = NumPyDistance
    BoundaryDistance: Final = NumPyBoundaryDistance
    Risk: Final = NumPyRisk
    CostFunction: Final = NumPyCostFunction
    PathParameterExtractor: Final = NumPyPathParameterExtractor
    PathVelocityExtractor: Final = NumPyPathVelocityExtractor
    PositionExtractor: Final = NumPyPositionExtractor
    DistanceExtractor: Final = NumPyDistanceExtractor
    BoundaryDistanceExtractor: Final = NumPyBoundaryDistanceExtractor
    RiskMetric: Final = NumPyRiskMetric
    ContouringCost: Final = NumPyContouringCost
    ObstacleStateProvider: Final = NumPyObstacleStateProvider

    class simple:
        State: Final = NumPySimpleState
        StateSequence: Final = NumPySimpleStateSequence
        StateBatch: Final = NumPySimpleStateBatch
        ControlInputSequence: Final = NumPySimpleControlInputSequence
        ControlInputBatch: Final = NumPySimpleControlInputBatch
        Costs: Final = NumPySimpleCosts
        SampledObstacleStates: Final = NumPySimpleSampledObstacleStates
        ObstacleStatesForTimeStep: Final = NumPySimpleObstacleStatesForTimeStep
        ObstacleStates: Final = NumPySimpleObstacleStates

    class integrator:
        ObstacleStateSequences: Final = NumPyIntegratorObstacleStateSequences

    class bicycle:
        State: Final = NumPyBicycleState
        StateSequence: Final = NumPyBicycleStateSequence
        StateBatch: Final = NumPyBicycleStateBatch
        Positions: Final = NumPyBicyclePositions
        ControlInputSequence: Final = NumPyBicycleControlInputSequence
        ControlInputBatch: Final = NumPyBicycleControlInputBatch
        ObstacleStateSequences: Final = NumPyBicycleObstacleStateSequences

    class unicycle:
        State: Final = NumPyUnicycleState
        StateSequence: Final = NumPyUnicycleStateSequence
        StateBatch: Final = NumPyUnicycleStateBatch
        Positions: Final = NumPyUnicyclePositions
        ControlInputSequence: Final = NumPyUnicycleControlInputSequence
        ControlInputBatch: Final = NumPyUnicycleControlInputBatch
        ObstacleStateSequences: Final = NumPyUnicycleObstacleStateSequences

    class augmented:
        State: Final = NumPyAugmentedState
        StateSequence: Final = NumPyAugmentedStateSequence
        StateBatch: Final = NumPyAugmentedStateBatch
        ControlInputSequence: Final = NumPyAugmentedControlInputSequence
        ControlInputBatch: Final = NumPyAugmentedControlInputBatch
