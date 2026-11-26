---
status: draft
---

# Observers

## Noisy Obstacle State Observer

Decorator that injects zero-mean Gaussian noise into obstacle state observations before delegating to the inner observer. Useful for testing estimator robustness.

### Usage

```python
from faran.numpy import obstacles, types
from numtypes import array

observer = obstacles.observer.noisy(
    provider,
    to_states=types.obstacle_2d_poses_for_time_step.wrap,
    sigma=array([0.1, 0.1, 0.05], shape=(3,)),
    seed=44,
)
```

::: faran.obstacles.observer.common.NoisyObstacleStateObserver
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - decorate
        - observe

## ID Assignment

### Hungarian Algorithm

Matches detected obstacles to tracked IDs across frames using the Hungarian algorithm[@Kuhn1955][@Munkres1957] on position distances. Detections beyond a configurable cutoff distance are assigned new IDs.

### Usage

```python
id_assignment = obstacles.id_assignment.hungarian(
    position_extractor=obstacle_position_extractor,
    cutoff=5.0,
)
```

/// backends

::: faran.obstacles.assignment.basic.NumPyHungarianObstacleIdAssignment
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.obstacles.assignment.accelerated.JaxHungarianObstacleIdAssignment
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

### ID Assignment Protocol

::: faran.types.ObstacleIdAssignment
    options:
      show_root_heading: true
      heading_level: 3

\bibliography
