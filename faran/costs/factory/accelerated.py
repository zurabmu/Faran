from typing import Final

from faran.types import (
    ControlInputBatch,
    StateBatch,
    CostFunction,
    JaxCosts,
)
from faran.costs.accelerated import (
    JaxContouringCost,
    JaxLagCost,
    JaxProgressCost,
    JaxControlSmoothingCost,
    JaxControlEffortCost,
    JaxPreferenceCost,
)
from faran.costs.combined import CombinedCost, JaxCostSumFunction
from faran.costs.collision import JaxCollisionCost
from faran.costs.distance import (
    JaxCircleDistanceExtractor,
    JaxSatDistanceExtractor,
)
from faran.costs.boundary import (
    JaxBoundaryCost,
    JaxFixedWidthBoundary,
    JaxPiecewiseFixedWidthBoundary,
)


class costs:
    @staticmethod
    def combined[
        ControlInputBatchT: ControlInputBatch,
        StateBatchT: StateBatch,
        CostsT: JaxCosts,
    ](
        *costs: CostFunction[ControlInputBatchT, StateBatchT, CostsT],
    ) -> CombinedCost[ControlInputBatchT, StateBatchT, CostsT]:
        """Creates a JAX cost function combining all given cost functions by summation."""
        return CombinedCost(costs=list(costs), sum=JaxCostSumFunction())

    class tracking:
        contouring: Final = JaxContouringCost.create
        lag: Final = JaxLagCost.create
        progress: Final = JaxProgressCost.create

    class comfort:
        control_smoothing: Final = JaxControlSmoothingCost.create
        control_effort: Final = JaxControlEffortCost.create

    class safety:
        collision: Final = JaxCollisionCost.create
        boundary: Final = JaxBoundaryCost.create

    preference: Final = JaxPreferenceCost.create


class distance:
    circles: Final = JaxCircleDistanceExtractor.create
    sat: Final = JaxSatDistanceExtractor.create


class boundary:
    fixed_width: Final = JaxFixedWidthBoundary.create
    piecewise_fixed_width: Final = JaxPiecewiseFixedWidthBoundary.create
