from typing import Final, Any

from faran.types import (
    JaxState,
    JaxStateSequence,
    JaxStateBatch,
    JaxControlInputSequence,
    JaxControlInputBatch,
    JaxCosts,
    JaxCostFunction,
    State as State,
    StateSequence as StateSequence,
    StateBatch as StateBatch,
    ControlInputSequence as ControlInputSequence,
    ControlInputBatch as ControlInputBatch,
    Costs as Costs,
    CostFunction as CostFunction,
    JaxPathParameters,
    JaxReferencePoints,
    JaxPositions,
    JaxSimplePositions,
    JaxHeadings,
    JaxLateralPositions,
    JaxLongitudinalPositions,
    JaxNormals,
    JaxRisk,
    JaxPathParameterExtractor,
    JaxPathVelocityExtractor,
    JaxPositionExtractor,
    JaxDistanceExtractor,
    JaxRiskMetric,
    Error as Error,  # NOTE: Aliased to workaround ruff bug.
    Risk as Risk,
    RiskMetric as RiskMetric,
    ContouringCost as ContouringCost,
    JaxSampledObstacleStates,
    JaxSampledObstaclePositions,
    JaxSampledObstacleHeadings,
    JaxSampledObstaclePositionExtractor,
    JaxSampledObstacleHeadingExtractor,
    JaxObstacleStates,
    JaxObstacleStatesForTimeStep,
    JaxObstacleStateProvider,
    JaxObstaclePositionExtractor,
    JaxBoundaryDistance,
    JaxBoundaryDistanceExtractor,
)
from faran.mppi import JaxWeights
from faran.models import (
    JaxBicycleState,
    JaxBicycleStateSequence,
    JaxBicycleStateBatch,
    JaxBicyclePositions,
    JaxBicycleControlInputSequence,
    JaxBicycleControlInputBatch,
    JaxBicycleObstacleStates,
    JaxBicycleObstacleInputs,
    JaxBicycleObstacleStateSequences,
    JaxIntegratorObstacleStateSequences,
    JaxUnicycleState,
    JaxUnicycleStateSequence,
    JaxUnicycleStateBatch,
    JaxUnicyclePositions,
    JaxUnicycleControlInputSequence,
    JaxUnicycleControlInputBatch,
    JaxUnicycleObstacleStates,
    JaxUnicycleObstacleInputs,
    JaxUnicycleObstacleStateSequences,
)
from faran.costs import (
    JaxPreference,
    JaxContouringCost,
    JaxDistance,
)
from faran.obstacles import (
    JaxObstacleIds,
    JaxSampledObstacle2dPoses,
    JaxObstacle2dPoses,
    JaxObstacle2dPosesForTimeStep,
    JaxObstacle2dPositions,
    JaxObstacle2dPositionsForTimeStep,
    JaxObstacleHeadings,
    JaxObstacleHeadingsForTimeStep,
    JaxObstacleStatesRunningHistory,
)
from faran.states import (
    JaxSimpleState,
    JaxSimpleStateSequence,
    JaxSimpleStateBatch,
    JaxSimpleControlInputSequence,
    JaxSimpleControlInputBatch,
    JaxSimpleCosts,
    JaxSimpleSampledObstacleStates,
    JaxSimpleObstacleStatesForTimeStep,
    JaxSimpleObstacleStates,
    JaxAugmentedState,
    JaxAugmentedStateSequence,
    JaxAugmentedStateBatch,
    JaxAugmentedControlInputSequence,
    JaxAugmentedControlInputBatch,
)


class types:
    type State = JaxState
    type StateSequence = JaxStateSequence
    type StateBatch = JaxStateBatch
    type ControlInputSequence = JaxControlInputSequence
    type ControlInputBatch = JaxControlInputBatch
    type Costs = JaxCosts
    type PathParameters = JaxPathParameters
    type ReferencePoints = JaxReferencePoints
    type Positions = JaxPositions
    type Headings = JaxHeadings
    type LateralPositions = JaxLateralPositions
    type LongitudinalPositions = JaxLongitudinalPositions
    type ObstacleIds = JaxObstacleIds
    type SampledObstacleStates = JaxSampledObstacleStates
    type SampledObstaclePositions = JaxSampledObstaclePositions
    type SampledObstacleHeadings = JaxSampledObstacleHeadings
    type SampledObstaclePositionExtractor[SampledStatesT] = (
        JaxSampledObstaclePositionExtractor[SampledStatesT]
    )
    type SampledObstacleHeadingExtractor[SampledStatesT] = (
        JaxSampledObstacleHeadingExtractor[SampledStatesT]
    )
    type ObstacleStates[SingleSampleT = Any, ObstacleStatesForTimeStepT = Any] = (
        JaxObstacleStates[SingleSampleT, ObstacleStatesForTimeStepT]
    )
    type ObstacleStatesForTimeStep[ObstacleStatesT = Any, NumPyT = Any] = (
        JaxObstacleStatesForTimeStep[ObstacleStatesT, NumPyT]
    )
    type ObstaclePositionExtractor[
        ObstacleStatesForTimeStepT,
        ObstacleStatesT,
        PositionsForTimeStepT,
        PositionsT,
    ] = JaxObstaclePositionExtractor[
        ObstacleStatesForTimeStepT,
        ObstacleStatesT,
        PositionsForTimeStepT,
        PositionsT,
    ]
    type SampledObstacle2dPoses = JaxSampledObstacle2dPoses
    type Obstacle2dPoses = JaxObstacle2dPoses
    type Obstacle2dPosesForTimeStep = JaxObstacle2dPosesForTimeStep
    type Obstacle2dPositions = JaxObstacle2dPositions
    type Obstacle2dPositionsForTimeStep = JaxObstacle2dPositionsForTimeStep
    type ObstacleHeadings = JaxObstacleHeadings
    type ObstacleHeadingsForTimeStep = JaxObstacleHeadingsForTimeStep
    type ObstacleStatesRunningHistory[
        StatesT: JaxObstacleStates,
        StatesForTimeStepT: JaxObstacleStatesForTimeStep,
    ] = JaxObstacleStatesRunningHistory[StatesT, StatesForTimeStepT]
    type Distance = JaxDistance
    type BoundaryDistance = JaxBoundaryDistance
    type Risk = JaxRisk
    type Preference = JaxPreference

    type Weights = JaxWeights
    type CostFunction = JaxCostFunction
    type PathParameterExtractor[StateBatchT] = JaxPathParameterExtractor[StateBatchT]
    type PathVelocityExtractor[InputBatchT] = JaxPathVelocityExtractor[InputBatchT]
    type PositionExtractor[StateBatchT] = JaxPositionExtractor[StateBatchT]
    type DistanceExtractor[StateBatchT, SampledObstacleStatesT, DistanceT] = (
        JaxDistanceExtractor[StateBatchT, SampledObstacleStatesT, DistanceT]
    )
    type BoundaryDistanceExtractor[StateBatchT, DistanceT] = (
        JaxBoundaryDistanceExtractor[StateBatchT, DistanceT]
    )
    type RiskMetric[StateBatchT, ObstacleStatesT, SampledObstacleStatesT] = (
        JaxRiskMetric[StateBatchT, ObstacleStatesT, SampledObstacleStatesT]
    )
    type ContouringCost[StateBatchT] = JaxContouringCost[StateBatchT]
    type ObstacleStateProvider[ObstacleStatesT] = JaxObstacleStateProvider[
        ObstacleStatesT
    ]

    path_parameters: Final = JaxPathParameters.create
    reference_points: Final = JaxReferencePoints.create
    positions: Final = JaxSimplePositions.create
    headings: Final = JaxHeadings.create
    lateral_positions: Final = JaxLateralPositions.create
    longitudinal_positions: Final = JaxLongitudinalPositions.create
    normals: Final = JaxNormals.create
    distance: Final = JaxDistance
    boundary_distance: Final = JaxBoundaryDistance
    preference: Final = JaxPreference.create
    obstacle_ids: Final = JaxObstacleIds
    obstacle_2d_poses: Final = JaxObstacle2dPoses
    obstacle_2d_poses_for_time_step: Final = JaxObstacle2dPosesForTimeStep
    obstacle_states_running_history: Final = JaxObstacleStatesRunningHistory

    class simple:
        type State = JaxSimpleState
        type StateSequence = JaxSimpleStateSequence
        type StateBatch = JaxSimpleStateBatch
        type ControlInputSequence = JaxSimpleControlInputSequence
        type ControlInputBatch = JaxSimpleControlInputBatch
        type Costs = JaxSimpleCosts
        type SampledObstacleStates = JaxSimpleSampledObstacleStates
        type ObstacleStatesForTimeStep = JaxSimpleObstacleStatesForTimeStep
        type ObstacleStates = JaxSimpleObstacleStates

        state: Final = JaxSimpleState
        state_sequence: Final = JaxSimpleStateSequence
        state_batch: Final = JaxSimpleStateBatch
        control_input_sequence: Final = JaxSimpleControlInputSequence
        control_input_batch: Final = JaxSimpleControlInputBatch
        costs: Final = JaxSimpleCosts
        obstacle_states: Final = JaxSimpleObstacleStates
        obstacle_states_for_time_step: Final = JaxSimpleObstacleStatesForTimeStep

    class integrator:
        type ObstacleStateSequences = JaxIntegratorObstacleStateSequences

    class bicycle:
        type State = JaxBicycleState
        type StateSequence = JaxBicycleStateSequence
        type StateBatch = JaxBicycleStateBatch
        type Positions = JaxBicyclePositions
        type ControlInputSequence = JaxBicycleControlInputSequence
        type ControlInputBatch = JaxBicycleControlInputBatch
        type ObstacleStates = JaxBicycleObstacleStates
        type ObstacleInputs = JaxBicycleObstacleInputs
        type ObstacleStateSequences = JaxBicycleObstacleStateSequences

        state: Final = JaxBicycleState
        state_sequence: Final = JaxBicycleStateSequence
        state_batch: Final = JaxBicycleStateBatch
        positions: Final = JaxBicyclePositions
        control_input_sequence: Final = JaxBicycleControlInputSequence
        control_input_batch: Final = JaxBicycleControlInputBatch
        obstacle_states: Final = JaxBicycleObstacleStates
        obstacle_inputs: Final = JaxBicycleObstacleInputs
        obstacle_state_sequences: Final = JaxBicycleObstacleStateSequences

    class unicycle:
        type State = JaxUnicycleState
        type StateSequence = JaxUnicycleStateSequence
        type StateBatch = JaxUnicycleStateBatch
        type Positions = JaxUnicyclePositions
        type ControlInputSequence = JaxUnicycleControlInputSequence
        type ControlInputBatch = JaxUnicycleControlInputBatch
        type ObstacleStates = JaxUnicycleObstacleStates
        type ObstacleInputs = JaxUnicycleObstacleInputs
        type ObstacleStateSequences = JaxUnicycleObstacleStateSequences

        state: Final = JaxUnicycleState
        state_sequence: Final = JaxUnicycleStateSequence
        state_batch: Final = JaxUnicycleStateBatch
        positions: Final = JaxUnicyclePositions
        control_input_sequence: Final = JaxUnicycleControlInputSequence
        control_input_batch: Final = JaxUnicycleControlInputBatch
        obstacle_states: Final = JaxUnicycleObstacleStates
        obstacle_inputs: Final = JaxUnicycleObstacleInputs
        obstacle_state_sequences: Final = JaxUnicycleObstacleStateSequences

    class augmented:
        type State[P: JaxState, V: JaxState] = JaxAugmentedState[P, V]
        type StateSequence[P: JaxStateSequence, V: JaxStateSequence] = (
            JaxAugmentedStateSequence[P, V]
        )
        type StateBatch[P: JaxStateBatch, V: JaxStateBatch] = JaxAugmentedStateBatch[
            P, V
        ]
        type ControlInputSequence[
            P: JaxControlInputSequence,
            V: JaxControlInputSequence,
        ] = JaxAugmentedControlInputSequence[P, V]
        type ControlInputBatch[P: JaxControlInputBatch, V: JaxControlInputBatch] = (
            JaxAugmentedControlInputBatch[P, V]
        )

        state: Final = JaxAugmentedState
        state_sequence: Final = JaxAugmentedStateSequence
        state_batch: Final = JaxAugmentedStateBatch
        control_input_sequence: Final = JaxAugmentedControlInputSequence
        control_input_batch: Final = JaxAugmentedControlInputBatch


class classes:
    State: Final = JaxState
    StateSequence: Final = JaxStateSequence
    StateBatch: Final = JaxStateBatch
    ControlInputSequence: Final = JaxControlInputSequence
    ControlInputBatch: Final = JaxControlInputBatch
    Costs: Final = JaxCosts
    PathParameters: Final = JaxPathParameters
    ReferencePoints: Final = JaxReferencePoints
    Positions: Final = JaxPositions
    Headings: Final = JaxHeadings
    LateralPositions: Final = JaxLateralPositions
    LongitudinalPositions: Final = JaxLongitudinalPositions
    ObstacleIds: Final = JaxObstacleIds
    ObstacleStates: Final = JaxObstacleStates
    ObstacleStatesForTimeStep: Final = JaxObstacleStatesForTimeStep
    SampledObstacleStates: Final = JaxSampledObstacleStates
    SampledObstaclePositions: Final = JaxSampledObstaclePositions
    SampledObstacleHeadings: Final = JaxSampledObstacleHeadings
    SampledObstaclePositionExtractor: Final = JaxSampledObstaclePositionExtractor
    SampledObstacleHeadingExtractor: Final = JaxSampledObstacleHeadingExtractor
    SampledObstacle2dPoses: Final = JaxSampledObstacle2dPoses
    Obstacle2dPoses: Final = JaxObstacle2dPoses
    Obstacle2dPosesForTimeStep: Final = JaxObstacle2dPosesForTimeStep
    Obstacle2dPositions: Final = JaxObstacle2dPositions
    Obstacle2dPositionsForTimeStep: Final = JaxObstacle2dPositionsForTimeStep
    ObstacleHeadings: Final = JaxObstacleHeadings
    ObstacleHeadingsForTimeStep: Final = JaxObstacleHeadingsForTimeStep
    ObstacleStatesRunningHistory: Final = JaxObstacleStatesRunningHistory
    ObstaclePositionExtractor: Final = JaxObstaclePositionExtractor
    Distance: Final = JaxDistance
    BoundaryDistance: Final = JaxBoundaryDistance
    Risk: Final = JaxRisk
    CostFunction: Final = JaxCostFunction
    PathParameterExtractor: Final = JaxPathParameterExtractor
    PathVelocityExtractor: Final = JaxPathVelocityExtractor
    PositionExtractor: Final = JaxPositionExtractor
    DistanceExtractor: Final = JaxDistanceExtractor
    BoundaryDistanceExtractor: Final = JaxBoundaryDistanceExtractor
    RiskMetric: Final = JaxRiskMetric
    ContouringCost: Final = JaxContouringCost
    ObstacleStateProvider: Final = JaxObstacleStateProvider

    class simple:
        State: Final = JaxSimpleState
        StateSequence: Final = JaxSimpleStateSequence
        StateBatch: Final = JaxSimpleStateBatch
        ControlInputSequence: Final = JaxSimpleControlInputSequence
        ControlInputBatch: Final = JaxSimpleControlInputBatch
        Costs: Final = JaxSimpleCosts
        SampledObstacleStates: Final = JaxSimpleSampledObstacleStates
        ObstacleStatesForTimeStep: Final = JaxSimpleObstacleStatesForTimeStep
        ObstacleStates: Final = JaxSimpleObstacleStates

    class integrator:
        ObstacleStateSequences: Final = JaxIntegratorObstacleStateSequences

    class bicycle:
        State: Final = JaxBicycleState
        StateSequence: Final = JaxBicycleStateSequence
        StateBatch: Final = JaxBicycleStateBatch
        Positions: Final = JaxBicyclePositions
        ControlInputSequence: Final = JaxBicycleControlInputSequence
        ControlInputBatch: Final = JaxBicycleControlInputBatch
        ObstacleStateSequences: Final = JaxBicycleObstacleStateSequences

    class unicycle:
        State: Final = JaxUnicycleState
        StateSequence: Final = JaxUnicycleStateSequence
        StateBatch: Final = JaxUnicycleStateBatch
        Positions: Final = JaxUnicyclePositions
        ControlInputSequence: Final = JaxUnicycleControlInputSequence
        ControlInputBatch: Final = JaxUnicycleControlInputBatch
        ObstacleStateSequences: Final = JaxUnicycleObstacleStateSequences

    class augmented:
        State: Final = JaxAugmentedState
        StateSequence: Final = JaxAugmentedStateSequence
        StateBatch: Final = JaxAugmentedStateBatch
        ControlInputSequence: Final = JaxAugmentedControlInputSequence
        ControlInputBatch: Final = JaxAugmentedControlInputBatch
