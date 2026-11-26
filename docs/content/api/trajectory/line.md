---
status: draft
---

# Line Trajectory

Straight-line reference path between two endpoints. Heading is constant along the path and given by equation [](#equation-line-heading).

/// equation | equation-line-heading

$$
\theta = \operatorname{atan2}(y_\text{end} - y_\text{start},\; x_\text{end} - x_\text{start})
$$

- $\theta$ is the heading of the path.
- $(x_\text{start}, y_\text{start})$ is the starting point.
- $(x_\text{end}, y_\text{end})$ is the ending point.

///

## Usage

```python
from faran.numpy import trajectory

reference = trajectory.line(start=(0.0, 0.0), end=(10.0, 0.0), path_length=10.0)
```

## NumPy

::: faran.trajectories.line.basic.NumPyLineTrajectory
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - query

## JAX

::: faran.trajectories.line.accelerated.JaxLineTrajectory
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - query
