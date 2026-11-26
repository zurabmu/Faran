---
status: draft
---

# Unicycle Model

Three-state model representing a point robot with direct velocity and angular velocity control[@Oriolo2002]. Discretized via Euler integration.

## Dynamics

The state is $[x, y, \theta]$ (position and heading), and the control input is $[v, \omega]$ (linear and angular velocity). Equation [](#equation-unicycle-transition) gives the state transition.

/// equation | equation-unicycle-transition

$$
\begin{aligned}
x_{t+1} &= x_t + v_t \cos(\theta_t) \, \Delta t \\
y_{t+1} &= y_t + v_t \sin(\theta_t) \, \Delta t \\
\theta_{t+1} &= \theta_t + \omega_t \, \Delta t
\end{aligned}
$$

- $(x_t, y_t)$ is the position at time step $t$.
- $\theta_t$ is the heading.
- $v_t$ is the linear velocity.
- $\omega_t$ is the angular velocity.
- $\Delta t$ is the time step size.

///

/// live | Unicycle

```python
--8<-- "docs/snippets/unicycle.py"
```

///

/// backends

::: faran.models.unicycle.basic.NumPyUnicycleModel
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

::: faran.models.unicycle.accelerated.JaxUnicycleModel
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

///

## Obstacle Model

Propagates obstacle states forward using unicycle kinematics. Follows the CTRV (Constant Turn Rate & Velocity) assumption[@Schubert2008]: state $\mathsf{x} = [x, y, \theta, v, \omega]$ with $v$ and $\omega$ held constant over the prediction horizon.

/// backends

::: faran.models.unicycle.basic.NumPyUnicycleObstacleModel
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.models.unicycle.accelerated.JaxUnicycleObstacleModel
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

\bibliography
