from typing import Final

from faran.models.integrator import (
    NumPyIntegratorModel,
    NumPyIntegratorObstacleModel,
    NumPyFiniteDifferenceIntegratorStateEstimator,
    NumPyKfIntegratorStateEstimator,
)
from faran.models.bicycle import (
    NumPyBicycleModel,
    NumPyBicycleObstacleModel,
    NumPyFiniteDifferenceBicycleStateEstimator,
    NumPyKfBicycleStateEstimator,
)
from faran.models.unicycle import (
    NumPyUnicycleModel,
    NumPyUnicycleObstacleModel,
    NumPyFiniteDifferenceUnicycleStateEstimator,
    NumPyKfUnicycleStateEstimator,
)


class model:
    class integrator:
        dynamical: Final = NumPyIntegratorModel.create
        obstacle: Final = NumPyIntegratorObstacleModel.create

        class estimator:
            finite_difference: Final = (
                NumPyFiniteDifferenceIntegratorStateEstimator.create
            )
            kf: Final = NumPyKfIntegratorStateEstimator.create

    class bicycle:
        dynamical: Final = NumPyBicycleModel.create
        obstacle: Final = NumPyBicycleObstacleModel.unscented

        class estimator:
            finite_difference: Final = NumPyFiniteDifferenceBicycleStateEstimator.create
            ekf: Final = NumPyKfBicycleStateEstimator.ekf
            ukf: Final = NumPyKfBicycleStateEstimator.ukf

    class unicycle:
        dynamical: Final = NumPyUnicycleModel.create
        obstacle: Final = NumPyUnicycleObstacleModel.unscented

        class estimator:
            finite_difference: Final = (
                NumPyFiniteDifferenceUnicycleStateEstimator.create
            )
            ekf: Final = NumPyKfUnicycleStateEstimator.ekf
            ukf: Final = NumPyKfUnicycleStateEstimator.ukf
