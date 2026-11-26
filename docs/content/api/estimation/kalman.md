---
status: draft
---

# Kalman Filter

Linear state estimator for the [integrator](../model/integrator.md) model[@Thrun2005]. Maintains a Gaussian belief $(\boldsymbol{\mu}, \boldsymbol{\Sigma})$ via prediction and update.

## Equations

The filter predicts the belief with equation [](#equation-kalman-predict) and then updates it with the observation $\mathbf{z}_t$ using equation [](#equation-kalman-update).

/// equation | equation-kalman-predict

$$
\begin{aligned}
\hat{\boldsymbol{\mu}}_t &= A \, \boldsymbol{\mu}_{t-1} \\
\hat{\boldsymbol{\Sigma}}_t &= A \, \boldsymbol{\Sigma}_{t-1} \, A^\top + R
\end{aligned}
$$

- $\hat{\boldsymbol{\mu}}_t$ is the predicted state mean.
- $\hat{\boldsymbol{\Sigma}}_t$ is the predicted state covariance.
- $A$ is the state transition matrix, built from `time_step_size`.
- $R$ is the process noise covariance.

///

/// equation | equation-kalman-update

$$
\begin{aligned}
K_t &= \hat{\boldsymbol{\Sigma}}_t \, H^\top \bigl(H \, \hat{\boldsymbol{\Sigma}}_t \, H^\top + Q\bigr)^{-1} \\
\boldsymbol{\mu}_t &= \hat{\boldsymbol{\mu}}_t + K_t \bigl(\mathbf{z}_t - H \, \hat{\boldsymbol{\mu}}_t\bigr) \\
\boldsymbol{\Sigma}_t &= (I - K_t H) \, \hat{\boldsymbol{\Sigma}}_t
\end{aligned}
$$

- $K_t$ is the Kalman gain.
- $H$ is the observation matrix, which maps the full state to the observed positions.
- $Q$ is the observation noise covariance.
- $\mathbf{z}_t$ is the observation at time step $t$.
- $I$ is the identity matrix.

///

## Parameters

```python
from faran.numpy import model

estimator = model.integrator.estimator.kf(
    time_step_size=0.1,
    process_noise_covariance=1e-3,
    observation_noise_covariance=1e-2,
)
```

/// backends

::: faran.models.integrator.basic.NumPyKfIntegratorStateEstimator
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

::: faran.models.integrator.accelerated.JaxKfIntegratorStateEstimator
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

///

For nonlinear models (bicycle, unicycle), use the [EKF](ekf.md) or [UKF](ukf.md).

\bibliography
