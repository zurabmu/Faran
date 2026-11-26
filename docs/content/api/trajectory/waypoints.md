---
status: draft
---

# Waypoints Trajectory

Cubic-spline path through a sequence of 2D waypoints. Cumulative arc lengths are computed from the waypoints to build natural cubic spline interpolants[@deBoor1978] for $x(\phi)$ and $y(\phi)$. Heading is derived from the spline tangent with equation [](#equation-waypoints-heading).

/// equation | equation-waypoints-heading

$$
\theta(\phi) = \operatorname{atan2}\!\bigl(y'(\phi),\; x'(\phi)\bigr)
$$

- $\theta(\phi)$ is the heading at arc length $\phi$.
- $x'(\phi)$ and $y'(\phi)$ are the derivatives of the spline interpolants.

///

Closest-point queries use a coarse KD-tree[@Bentley1975] (NumPy) or brute-force (JAX) lookup followed by Newton refinement[@Nocedal2006].

## Usage

/// live | Waypoints trajectory
    still: true

```python
--8<-- "docs/snippets/waypoints.py"
```

///

## NumPy

::: faran.trajectories.waypoints.basic.NumPyWaypointsTrajectory
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - query

## JAX

::: faran.trajectories.waypoints.accelerated.JaxWaypointsTrajectory
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - query

\bibliography
