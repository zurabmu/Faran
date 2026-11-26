---
status: draft
---

# Obstacle Simulators

Ground-truth obstacle generators for testing and simulation. In production, observations come from a perception system.

## Static Obstacle Simulator

Obstacles with fixed positions that do not move.

### Usage

```python
from faran.numpy import obstacles
from numtypes import array

simulator = obstacles.static(
    positions=array([[3.0, 1.0], [7.0, -1.0]], shape=(2, 2)),
)
```

/// backends

::: faran.obstacles.static.basic.NumPyStaticObstacleSimulator
    options:
      show_root_heading: true
      heading_level: 3

::: faran.obstacles.static.accelerated.JaxStaticObstacleSimulator
    options:
      show_root_heading: true
      heading_level: 3

///

## Dynamic Obstacle Simulator

Obstacles moving with constant velocity. Heading is derived from velocity direction.

### Usage

```python
simulator = obstacles.dynamic(
    positions=array([[5.0, 2.0]], shape=(1, 2)),
    velocities=array([[-1.0, 0.0]], shape=(1, 2)),
)
```

/// backends

::: faran.obstacles.dynamic.basic.NumPyDynamicObstacleSimulator
    options:
      show_root_heading: true
      heading_level: 3

::: faran.obstacles.dynamic.accelerated.JaxDynamicObstacleSimulator
    options:
      show_root_heading: true
      heading_level: 3

///
