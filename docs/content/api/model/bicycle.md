---
status: draft
---

# Kinematic Bicycle Model

Four-state model representing a wheeled vehicle with acceleration and steering control[@Kong2015]. Discretized via Euler integration.

## Dynamics

The state is $[x, y, \theta, v]$ (position, heading and speed), and the control input is $[a, \delta]$ (acceleration and steering angle). Equation [](#equation-slip-angle) gives the slip angle $\beta$ at the reference point, and equation [](#equation-bicycle-transition) gives the state transition.

/// equation | equation-slip-angle

$$
\beta = \arctan\!\left(\frac{l_r}{L} \tan(\delta)\right)
$$

- $\beta$ is the slip angle at the reference point.
- $l_r$ is the distance from the reference point to the rear axle.
- $L$ is the wheelbase.
- $\delta$ is the steering angle.

///

/// equation | equation-bicycle-transition

$$
\begin{aligned}
x_{t+1} &= x_t + v_t \cos(\theta_t + \beta) \, \Delta t \\
y_{t+1} &= y_t + v_t \sin(\theta_t + \beta) \, \Delta t \\
\theta_{t+1} &= \theta_t + \frac{v_t}{L} \cos(\beta) \tan(\delta_t) \, \Delta t \\
v_{t+1} &= v_t + a_t \, \Delta t
\end{aligned}
$$

- $(x_t, y_t)$ is the position of the reference point at time step $t$.
- $\theta_t$ is the heading.
- $v_t$ is the speed.
- $a_t$ is the acceleration.
- $\delta_t$ is the steering angle.
- $\Delta t$ is the time step size.

///

When $l_r = 0$, equation [](#equation-slip-angle) gives $\beta = 0$, and equation [](#equation-bicycle-transition) reduces to the standard rear-axle model.

/// live | Kinematic bicycle

```python
--8<-- "docs/snippets/bicycle.py"
```

///

/// backends

::: faran.models.bicycle.basic.NumPyBicycleModel
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

::: faran.models.bicycle.accelerated.JaxBicycleModel
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

///

## Obstacle Model

Propagates obstacle states forward using bicycle kinematics. Paired with a [state estimator](../estimation/index.md) and [predictor](../predictor/index.md) for obstacle tracking.

The obstacle model follows the CSAA (Constant Steering Angle & Acceleration) assumption[@Schubert2008]: state $\mathsf{x} = [x, y, \theta, v, a, \delta]$ with $a$ and $\delta$ held constant over the prediction horizon.

/// backends

::: faran.models.bicycle.basic.NumPyBicycleObstacleModel
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.models.bicycle.accelerated.JaxBicycleObstacleModel
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

\bibliography
