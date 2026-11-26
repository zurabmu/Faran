---
status: draft
---

# Safety Costs

## Collision Cost

Hinge-loss collision avoidance[@Schulman2013]. The cost in equation [](#equation-collision) activates when any vehicle part's signed distance falls below its threshold.

/// equation | equation-collision

$$
J_{\text{col}} = \sum_{i=1}^{V} k_{\text{col}} \max(0,\; d_0^{(i)} - d_i)
$$

- $V$ is the number of vehicle parts.
- $d_i$ is the signed distance of vehicle part $i$.
- $d_0^{(i)}$ is the distance threshold of vehicle part $i$.
- $k_{\text{col}}$ is the collision weight.

///

```python
from faran.numpy import costs, obstacles, risk
import numpy as np

collision = costs.safety.collision(
    obstacle_states=provider,
    sampler=obstacles.sampler.gaussian(seed=44),
    distance=distance_extractor,
    distance_threshold=np.array([0.5, 0.5, 0.5]),
    weight=1500.0,
    metric=risk.cvar(alpha=0.95, sample_count=50),
)
```

/// backends

::: faran.costs.collision.basic.NumPyCollisionCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.costs.collision.accelerated.JaxCollisionCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Boundary Cost

Applies the hinge loss of equation [](#equation-collision) to the distance from the corridor boundary, with threshold $d_0$ and weight $k_{\text{boundary}}$. See [Boundary](../boundary/index.md) for available boundary types.

/// backends

::: faran.costs.boundary.basic.NumPyBoundaryCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.costs.boundary.accelerated.JaxBoundaryCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Distance Functions

### Circle Distance

Pairwise signed distances between circular approximations of ego and obstacle[@Tolksdorf2024].

/// backends

::: faran.costs.distance.circles.basic.NumPyCircleDistanceExtractor
    options:
      show_root_heading: true
      heading_level: 4
      members:
        - create

::: faran.costs.distance.circles.accelerated.JaxCircleDistanceExtractor
    options:
      show_root_heading: true
      heading_level: 4
      members:
        - create

///

### SAT Distance

Signed distances between convex polygons via the Separating Axis Theorem[@Gottschalk1997].

/// backends

::: faran.costs.distance.sat.basic.NumPySatDistanceExtractor
    options:
      show_root_heading: true
      heading_level: 4
      members:
        - create

::: faran.costs.distance.sat.accelerated.JaxSatDistanceExtractor
    options:
      show_root_heading: true
      heading_level: 4
      members:
        - create

///

\bibliography
