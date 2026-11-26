---
status: draft
---

# Finite Difference Estimator

Numerical differentiation of consecutive observations. Requires no tuning and produces no covariance — use a [Kalman-family estimator](kalman.md) when uncertainty is needed.

## Formulas

All models estimate the speed with equation [](#equation-speed), which needs $T \geq 2$ observations. The sign of the speed comes from projecting the displacement onto the heading direction.

/// equation | equation-speed

$$
v_t = \operatorname{sign}\!\bigl(\Delta x_t \cos\theta_t + \Delta y_t \sin\theta_t\bigr) \; \frac{\lVert \Delta \mathbf{p}_t \rVert}{\Delta t}
$$

- $v_t$ is the speed at time step $t$.
- $\Delta \mathbf{p}_t$ is the displacement between the last two observed positions, with components $\Delta x_t$ and $\Delta y_t$.
- $\theta_t$ is the observed heading.
- $\Delta t$ is the time step size.

///

The unicycle estimates the angular velocity with equation [](#equation-angular-velocity), which needs $T \geq 2$ observations.

/// equation | equation-angular-velocity

$$
\omega_t = \frac{\theta_t - \theta_{t-1}}{\Delta t}
$$

- $\omega_t$ is the angular velocity at time step $t$.
- $\theta_t$ is the observed heading.

///

The bicycle estimates the acceleration with equation [](#equation-acceleration), which needs $T \geq 3$ observations, and the steering angle with equation [](#equation-steering-angle), which needs $T \geq 2$.

/// equation | equation-acceleration

$$
a_t = \frac{v_t - v_{t-1}}{\Delta t}
$$

- $a_t$ is the acceleration at time step $t$.
- $v_t$ is the speed from equation [](#equation-speed).

///

Equation [](#equation-steering-angle) follows from the heading rate $\dot\theta_t$ and the kinematic bicycle geometry[@Kong2015].

/// equation | equation-steering-angle

$$
\delta_t = \arctan\!\left(\frac{L \, \dot\theta_t}{\sqrt{v_t^2 - l_r^2 \, \dot\theta_t^2}}\right)
$$

- $\delta_t$ is the steering angle at time step $t$.
- $\dot\theta_t$ is the heading rate.
- $L$ is the wheelbase.
- $l_r$ is the distance from the reference point to the rear axle.

///

The steering angle is set to zero when $|v_t| < \varepsilon$ or $v_t^2 \leq l_r^2 \dot\theta_t^2$.

## Bicycle

```python
from faran.numpy import model

estimator = model.bicycle.estimator.finite_difference(
    time_step_size=0.1, wheelbase=2.5, rear_axle_distance=1.0,
)
```

/// backends

::: faran.models.bicycle.basic.NumPyFiniteDifferenceBicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.models.bicycle.accelerated.JaxFiniteDifferenceBicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Unicycle

```python
estimator = model.unicycle.estimator.finite_difference(time_step_size=0.1)
```

/// backends

::: faran.models.unicycle.basic.NumPyFiniteDifferenceUnicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.models.unicycle.accelerated.JaxFiniteDifferenceUnicycleStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Integrator

The integrator estimates the velocity with equation [](#equation-integrator-velocity).

/// equation | equation-integrator-velocity

$$
\mathbf{v}_t = \frac{\mathbf{x}_t - \mathbf{x}_{t-1}}{\Delta t}
$$

- $\mathbf{v}_t$ is the velocity at time step $t$.
- $\mathbf{x}_t$ is the observed position.

///

```python
estimator = model.integrator.estimator.finite_difference(time_step_size=0.1)
```

/// backends

::: faran.models.integrator.basic.NumPyFiniteDifferenceIntegratorStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.models.integrator.accelerated.JaxFiniteDifferenceIntegratorStateEstimator
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

\bibliography
