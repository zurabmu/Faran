---
status: draft
---

# Unscented Kalman Filter

Second-order nonlinear state estimator for the [bicycle](../model/bicycle.md) and [unicycle](../model/unicycle.md) models[@Julier1996][@Wan2000]. Propagates $2n + 1$ sigma points through the nonlinear dynamics and reconstructs the output distribution, capturing mean and covariance to second order (vs. first order for [EKF](ekf.md)).

## Sigma Points

The spread of the sigma points follows from the scaling parameter in equation [](#equation-sigma-point-scaling)[@Wan2000]. The estimators use the default `alpha` and `beta` of the underlying filter.

/// equation | equation-sigma-point-scaling

$$
\lambda = \alpha^2 (n + \kappa) - n
$$

- $\lambda$ is the scaling parameter.
- $\alpha$ is the spread of the sigma points around the mean.
- $n$ is the state dimension.
- $\kappa$ is the secondary scaling parameter, which is 0.

///

/// backends

::: faran.filters.ukf.basic.NumPyUnscentedKalmanFilter
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.filters.ukf.accelerated.JaxUnscentedKalmanFilter
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Bicycle

Takes the same parameters as the [bicycle EKF](ekf.md#bicycle).

```python
from faran.numpy import model

estimator = model.bicycle.estimator.ukf(
    time_step_size=0.1,
    wheelbase=2.5,
    rear_axle_distance=1.0,
    process_noise_covariance=1e-3,
    observation_noise_covariance=1e-2,
)
```

/// backends

::: faran.models.bicycle.basic.NumPyKfBicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - ukf

::: faran.models.bicycle.accelerated.JaxKfBicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - ukf

///

## Unicycle

Takes the same parameters as the [unicycle EKF](ekf.md#unicycle).

```python
estimator = model.unicycle.estimator.ukf(
    time_step_size=0.1,
    process_noise_covariance=1e-3,
    observation_noise_covariance=1e-2,
)
```

/// backends

::: faran.models.unicycle.basic.NumPyKfUnicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - ukf

::: faran.models.unicycle.accelerated.JaxKfUnicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - ukf

///

\bibliography
