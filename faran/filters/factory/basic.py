from typing import Final

from faran.types import (
    NumPyNoiseCovariances,
    NumPyNoiseCovarianceDescription,
)
from faran.filters.kf import numpy_kalman_filter
from faran.filters.noise import (
    NumPyAdaptiveNoiseProvider,
    NumPyClampedNoiseProvider,
    NumPyNoiseCovarianceBounds,
    IdentityNoiseModelProvider,
)


class noise:
    adaptive: Final = NumPyAdaptiveNoiseProvider.create
    clamped: Final = NumPyClampedNoiseProvider.decorate
    identity: Final = IdentityNoiseModelProvider

    @staticmethod
    def covariances(
        *,
        process: NumPyNoiseCovarianceDescription,
        observation: NumPyNoiseCovarianceDescription,
        process_dimension: int | None = None,
        observation_dimension: int | None = None,
    ) -> NumPyNoiseCovariances:
        return NumPyNoiseCovariances(
            process_noise_covariance=numpy_kalman_filter.standardize_noise_covariance(
                process, dimension=process_dimension
            ),
            observation_noise_covariance=numpy_kalman_filter.standardize_noise_covariance(
                observation, dimension=observation_dimension
            ),
        )

    covariance_bounds: Final = NumPyNoiseCovarianceBounds.create
