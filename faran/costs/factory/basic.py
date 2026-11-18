from typing import Final

from faran.types import (
    ControlInputBatch,
    StateBatch,
    CostFunction,
    NumPyCosts,
)
from faran.costs.basic import (
    NumPyContouringCost,
    NumPyLagCost,
    NumPyProgressCost,
    NumPyControlSmoothingCost,
    NumPyControlEffortCost,
    NumPyPreferenceCost,
)
from faran.costs.combined import CombinedCost, NumPyCostSumFunction
from faran.costs.collision import NumPyCollisionCost
from faran.costs.distance import (
    NumPyCircleDistanceExtractor,
    NumPySatDistanceExtractor,
)
from faran.costs.boundary import (
    NumPyBoundaryCost,
    NumPyFixedWidthBoundary,
    NumPyPiecewiseFixedWidthBoundary,
)


class costs:
    @staticmethod
    def combined[
        ControlInputBatchT: ControlInputBatch,
        StateBatchT: StateBatch,
        CostsT: NumPyCosts,
    ](
        *costs: CostFunction[ControlInputBatchT, StateBatchT, CostsT],
    ) -> CombinedCost[ControlInputBatchT, StateBatchT, CostsT]:
        """Creates a NumPy cost function combining all given cost functions by summation."""
        return CombinedCost(costs=list(costs), sum=NumPyCostSumFunction())

    class tracking:
        contouring: Final = NumPyContouringCost.create
        lag: Final = NumPyLagCost.create
        progress: Final = NumPyProgressCost.create

    class comfort:
        control_smoothing: Final = NumPyControlSmoothingCost.create
        control_effort: Final = NumPyControlEffortCost.create

    class safety:
        collision: Final = NumPyCollisionCost.create
        boundary: Final = NumPyBoundaryCost.create

    preference: Final = NumPyPreferenceCost.create


class distance:
    circles: Final = NumPyCircleDistanceExtractor.create
    sat: Final = NumPySatDistanceExtractor.create


class boundary:
    fixed_width: Final = NumPyFixedWidthBoundary.create
    piecewise_fixed_width: Final = NumPyPiecewiseFixedWidthBoundary.create
