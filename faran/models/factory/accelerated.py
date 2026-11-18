from typing import Final

from faran.models.integrator import (
    JaxIntegratorModel,
    JaxIntegratorObstacleModel,
    JaxFiniteDifferenceIntegratorStateEstimator,
    JaxKfIntegratorStateEstimator,
)
from faran.models.bicycle import (
    JaxBicycleModel,
    JaxBicycleObstacleModel,
    JaxFiniteDifferenceBicycleStateEstimator,
    JaxKfBicycleStateEstimator,
)
from faran.models.unicycle import (
    JaxUnicycleModel,
    JaxUnicycleObstacleModel,
    JaxFiniteDifferenceUnicycleStateEstimator,
    JaxKfUnicycleStateEstimator,
)


class model:
    class integrator:
        dynamical: Final = JaxIntegratorModel.create
        obstacle: Final = JaxIntegratorObstacleModel.create

        class estimator:
            finite_difference: Final = (
                JaxFiniteDifferenceIntegratorStateEstimator.create
            )
            kf: Final = JaxKfIntegratorStateEstimator.create

    class bicycle:
        dynamical: Final = JaxBicycleModel.create
        obstacle: Final = JaxBicycleObstacleModel.unscented

        class estimator:
            finite_difference: Final = JaxFiniteDifferenceBicycleStateEstimator.create
            ekf: Final = JaxKfBicycleStateEstimator.ekf
            ukf: Final = JaxKfBicycleStateEstimator.ukf

    class unicycle:
        dynamical: Final = JaxUnicycleModel.create
        obstacle: Final = JaxUnicycleObstacleModel.unscented

        class estimator:
            finite_difference: Final = JaxFiniteDifferenceUnicycleStateEstimator.create
            ekf: Final = JaxKfUnicycleStateEstimator.ekf
            ukf: Final = JaxKfUnicycleStateEstimator.ukf
