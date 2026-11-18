from typing import Final

from faran.types import (
    JaxNoiseCovariances,
    JaxNoiseCovarianceDescription,
)
from faran.filters.kf import jax_kalman_filter
from faran.filters.noise import (
    JaxAdaptiveNoiseProvider,
    JaxClampedNoiseProvider,
    JaxNoiseCovarianceBounds,
    IdentityNoiseModelProvider,
)


class noise:
    adaptive: Final = JaxAdaptiveNoiseProvider.create
    clamped: Final = JaxClampedNoiseProvider.decorate
    identity: Final = IdentityNoiseModelProvider

    @staticmethod
    def covariances(
        *,
        process: JaxNoiseCovarianceDescription,
        observation: JaxNoiseCovarianceDescription,
        process_dimension: int | None = None,
        observation_dimension: int | None = None,
    ) -> JaxNoiseCovariances:
        return JaxNoiseCovariances(
            process_noise_covariance=jax_kalman_filter.standardize_noise_covariance(
                process, dimension=process_dimension
            ),
            observation_noise_covariance=jax_kalman_filter.standardize_noise_covariance(
                observation, dimension=observation_dimension
            ),
        )

    covariance_bounds: Final = JaxNoiseCovarianceBounds.create
