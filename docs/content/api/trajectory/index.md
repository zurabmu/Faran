---
status: draft
---

# trajectory

Reference paths parameterized by arc length $\phi \in [0, L]$, where $L$ is the user-specified path length. Querying at $\phi$ returns position $(x_\phi, y_\phi)$ and heading $\theta_\phi$.

## Available Trajectories

| Trajectory | Description | Factory |
|------------|-------------|---------|
| [Waypoints](waypoints.md) | Cubic-spline path through 2D waypoints | `trajectory.waypoints(...)` |
| [Line](line.md) | Straight segment between two endpoints | `trajectory.line(...)` |

## Properties

Every trajectory has a `path_length`, a `natural_length` and an `end` point, which the [Trajectory Protocol](#trajectory-protocol) describes.

## Querying

```python
ref_points = reference.query(path_parameters)
ref_points.x()        # shape: (T, M)
ref_points.y()        # shape: (T, M)
ref_points.heading()  # shape: (T, M)
```

## Cyclic Trajectories

For looped paths, enable periodicity in the MPCC config. See [MPCC](../../guide/concepts/mpcc.md).

## Trajectory Protocol

::: faran.types.Trajectory
    options:
      show_root_heading: true
      heading_level: 3
