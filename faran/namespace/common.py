from typing import TYPE_CHECKING, Final

from faran.types import (
    State as State,
    StateSequence as StateSequence,
    StateBatch as StateBatch,
    ControlInputSequence as ControlInputSequence,
    ControlInputBatch as ControlInputBatch,
    Costs as Costs,
    CostFunction as CostFunction,
    BICYCLE_D_X,
    BICYCLE_D_U,
    BicycleD_x,
    BicycleD_u,
    BicycleState,
    BicycleStateSequence,
    BicycleStateBatch,
    BicyclePositions,
    BicycleControlInputSequence,
    BicycleControlInputBatch,
    UNICYCLE_D_X,
    UNICYCLE_D_U,
    UnicycleD_x,
    UnicycleD_u,
    UnicycleState,
    UnicycleStateSequence,
    UnicycleStateBatch,
    UnicyclePositions,
    UnicycleControlInputSequence,
    UnicycleControlInputBatch,
    PoseD_o as PoseD_o_,
    POSE_D_O as POSE_D_O_,
    Error as Error,  # NOTE: Aliased to workaround ruff bug.
    Risk as Risk,
    RiskMetric as RiskMetric,
    ContouringCost as ContouringCost,
    AugmentedState,
    AugmentedStateSequence,
    AugmentedStateBatch,
    AugmentedControlInputSequence,
    AugmentedControlInputBatch,
)
from faran.optional import loaded_on_access
from faran.namespace.basic import types as numpy_types, classes as numpy_classes

if TYPE_CHECKING:
    from faran.namespace.accelerated import types as jax_types, classes as jax_classes


class types:
    """Namespace of type aliases for states, controls, costs, and related domain types."""

    type State = State
    type StateBatch = StateBatch
    type ControlInputSequence = ControlInputSequence
    type ControlInputBatch = ControlInputBatch
    type Costs = Costs
    type CostFunction[InputBatchT, StateBatchT, CostsT] = CostFunction[
        InputBatchT, StateBatchT, CostsT
    ]
    type Error = Error
    type Risk = Risk

    type ContouringCost[InputBatchT, StateBatchT, ErrorT] = ContouringCost[
        InputBatchT, StateBatchT, ErrorT
    ]
    type RiskMetric[CostFunctionT, StateBatchT, ObstacleStatesT, SamplerT, RiskT] = (
        RiskMetric[CostFunctionT, StateBatchT, ObstacleStatesT, SamplerT, RiskT]
    )

    class obstacle:
        type PoseD_o = PoseD_o_

        POSE_D_O: Final = POSE_D_O_

    class bicycle:
        type D_x = BicycleD_x
        type D_u = BicycleD_u
        type State = BicycleState
        type StateSequence = BicycleStateSequence
        type StateBatch = BicycleStateBatch
        type Positions = BicyclePositions
        type ControlInputSequence = BicycleControlInputSequence
        type ControlInputBatch = BicycleControlInputBatch

        D_X: Final = BICYCLE_D_X
        D_U: Final = BICYCLE_D_U

    class unicycle:
        type D_x = UnicycleD_x
        type D_u = UnicycleD_u
        type State = UnicycleState
        type StateSequence = UnicycleStateSequence
        type StateBatch = UnicycleStateBatch
        type Positions = UnicyclePositions
        type ControlInputSequence = UnicycleControlInputSequence
        type ControlInputBatch = UnicycleControlInputBatch

        D_X: Final = UNICYCLE_D_X
        D_U: Final = UNICYCLE_D_U

    class augmented:
        type State[P, V] = AugmentedState[P, V]
        type StateSequence[P, V] = AugmentedStateSequence[P, V]
        type StateBatch[P, V] = AugmentedStateBatch[P, V]
        type ControlInputSequence[P, V] = AugmentedControlInputSequence[P, V]
        type ControlInputBatch[P, V] = AugmentedControlInputBatch[P, V]

        state: Final = AugmentedState
        state_sequence: Final = AugmentedStateSequence
        state_batch: Final = AugmentedStateBatch
        control_input_sequence: Final = AugmentedControlInputSequence
        control_input_batch: Final = AugmentedControlInputBatch

    numpy = numpy_types

    if TYPE_CHECKING:
        jax = jax_types
    else:
        jax = loaded_on_access(module="faran.namespace.accelerated", name="types")


class classes:
    """Namespace of concrete protocol classes for states, controls, costs, and related types."""

    State: Final = State
    StateSequence: Final = StateSequence
    StateBatch: Final = StateBatch
    ControlInputSequence: Final = ControlInputSequence
    ControlInputBatch: Final = ControlInputBatch
    Costs: Final = Costs
    CostFunction: Final = CostFunction
    Error: Final = Error
    Risk: Final = Risk
    RiskMetric: Final = RiskMetric
    ContouringCost: Final = ContouringCost

    class bicycle:
        State: Final = BicycleState
        StateSequence: Final = BicycleStateSequence
        StateBatch: Final = BicycleStateBatch
        Positions: Final = BicyclePositions
        ControlInputSequence: Final = BicycleControlInputSequence
        ControlInputBatch: Final = BicycleControlInputBatch

    class unicycle:
        State: Final = UnicycleState
        StateSequence: Final = UnicycleStateSequence
        StateBatch: Final = UnicycleStateBatch
        Positions: Final = UnicyclePositions
        ControlInputSequence: Final = UnicycleControlInputSequence
        ControlInputBatch: Final = UnicycleControlInputBatch

    class augmented:
        State: Final = AugmentedState
        StateSequence: Final = AugmentedStateSequence
        StateBatch: Final = AugmentedStateBatch
        ControlInputSequence: Final = AugmentedControlInputSequence
        ControlInputBatch: Final = AugmentedControlInputBatch

    numpy = numpy_classes

    if TYPE_CHECKING:
        jax = jax_classes
    else:
        jax = loaded_on_access(module="faran.namespace.accelerated", name="classes")
