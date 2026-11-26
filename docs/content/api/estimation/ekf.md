---
status: draft
---

# Extended Kalman Filter

First-order nonlinear state estimator for the [bicycle](../model/bicycle.md) and [unicycle](../model/unicycle.md) models[@Thrun2005]. Linearizes around the current estimate via the Jacobian $F_t = \frac{\partial f}{\partial \mathbf{x}}\big|_{\boldsymbol{\mu}_{t-1}}$, then applies the [Kalman](kalman.md) predict-update cycle with $F_t$ in place of $A$. The covariance prediction becomes equation [](#equation-ekf-covariance-prediction).

/// equation | equation-ekf-covariance-prediction

$$
\hat{\boldsymbol{\Sigma}}_t = F_t \, \boldsymbol{\Sigma}_{t-1} \, F_t^\top + R
$$

- $\hat{\boldsymbol{\Sigma}}_t$ is the predicted state covariance.
- $F_t$ is the Jacobian of the dynamics at the previous estimate.
- $\boldsymbol{\Sigma}_{t-1}$ is the previous state covariance.
- $R$ is the process noise covariance.

///

## Bicycle

```python
from faran.numpy import model

estimator = model.bicycle.estimator.ekf(
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
        - ekf

::: faran.models.bicycle.accelerated.JaxKfBicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - ekf

///

## Unicycle

```python
estimator = model.unicycle.estimator.ekf(
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
        - ekf

::: faran.models.unicycle.accelerated.JaxKfUnicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - ekf

///

For second-order accuracy, see the [UKF](ukf.md).

\bibliography
