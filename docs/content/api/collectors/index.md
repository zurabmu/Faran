---
status: draft
---

# collectors

Decorator-based data recorders for simulation loops. Collectors wrap planners and obstacle observers — the wrapped object behaves identically but also stores data for [metrics](../metrics/index.md) and visualization.

## Available Collectors

| Factory | Wraps | Records |
|---------|-------|---------|
| `collectors.states.decorating(planner, ...)` | `Mppi` | Initial state per planning step |
| `collectors.controls.decorating(planner, ...)` | `Mppi` | `Control` output per step |
| `collectors.trajectories.decorating(planner, ...)` | `Mppi` | State trajectories per step |
| `collectors.risk.decorating(metric, ...)` | `RiskMetric` | Risk values per evaluation |
| `collectors.obstacle_states.decorating(observer, ...)` | `ObstacleStateObserver` | Ground-truth obstacle states |
| `collectors.obstacle_observations.decorating(observer, ...)` | `ObstacleStateObserver` | Post-processed observations |
| `collectors.obstacle_forecasts.decorating(provider, ...)` | `ObstacleStateProvider` | Predicted obstacle forecasts |

Import `collectors` from the backend you are using (e.g. `faran.numpy` or `faran.jax`).

All collectors accept an optional `transformer` that converts collected items before storage. Use the appropriate state-sequence builder for your model (e.g., `types.augmented.state_sequence.of_states` for MPCC).

## Usage

```python
from faran import metrics
from faran.numpy import collectors

planner = collectors.states.decorating(
    planner,
    transformer=types.augmented.state_sequence.of_states,
)
observer = collectors.obstacle_states.decorating(observer)

registry = metrics.registry(
    collision_metric := metrics.collision(...),
    collectors=collectors.registry(planner, observer),
)
```

## Data Access

Retrieve collected data via typed accessors:

```python
from faran import access

states = registry.data(access.states.require())
controls = registry.data(access.controls.optional())
```

Use `.require()` to raise if data was not collected, or `.optional()` if it may not be available. The [`access`](registry.md#faran.collectors.access) namespace lists every accessor and the collector that records its data.
