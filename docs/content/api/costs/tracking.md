---
status: draft
---

# Tracking Costs

MPCC path-following objectives[@Liniger2015]. Require extractors mapping augmented states to positions and path parameters — provided automatically by `mppi.mpcc(...)`.

## Contouring Cost

Lateral (orthogonal) deviation from the reference trajectory, as equation [](#equation-contouring) defines it.

/// equation | equation-contouring

$$
J_c = k_c \, e_c^2, \quad e_c = \sin(\theta_\phi)(x - x_\phi) - \cos(\theta_\phi)(y - y_\phi)
$$

- $e_c$ is the contouring error.
- $k_c$ is the contouring weight.
- $(x, y)$ is the vehicle position.
- $(x_\phi, y_\phi)$ is the point on the reference path at path parameter $\phi$.
- $\theta_\phi$ is the heading of the reference path at that point.

///

/// backends

::: faran.costs.basic.NumPyContouringCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - error

::: faran.costs.accelerated.JaxContouringCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - error

///

## Lag Cost

Longitudinal (tangential) deviation from the reference point, as equation [](#equation-lag) defines it. The remaining symbols are those of equation [](#equation-contouring).

/// equation | equation-lag

$$
J_l = k_l \, e_l^2, \quad e_l = -\cos(\theta_\phi)(x - x_\phi) - \sin(\theta_\phi)(y - y_\phi)
$$

- $e_l$ is the lag error.
- $k_l$ is the lag weight.

///

Same parameters as contouring cost with weight $k_l$.

/// backends

::: faran.costs.basic.NumPyLagCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - error

::: faran.costs.accelerated.JaxLagCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - error

///

## Progress Cost

Rewards forward motion along the reference path with the negative cost in equation [](#equation-progress).

/// equation | equation-progress

$$
J_p = -k_p \, \dot{\phi} \, \Delta t
$$

- $k_p$ is the progress weight.
- $\dot{\phi}$ is the path velocity.
- $\Delta t$ is the time step size.

///

/// backends

::: faran.costs.basic.NumPyProgressCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.costs.accelerated.JaxProgressCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

\bibliography
