---
status: draft
---

# metrics

Post-simulation evaluation metrics operating on data recorded by [collectors](../collectors/index.md). Metrics are registered in a `MetricRegistry` and computed lazily on first access.

## Available Metrics

| Metric | Factory | Result Type | Description |
|--------|---------|-------------|-------------|
| [Collision](#collision) | `metrics.collision(...)` | `CollisionMetricResult` | Minimum distances and collision flags |
| [Task Completion](#task-completion) | `metrics.task_completion(...)` | `TaskCompletionMetricResult` | Goal arrival, stretch ratio, progress |
| [MPCC Error](#mpcc-error) | `metrics.mpcc_error(...)` | `MpccErrorMetricResult` | Contouring and lag tracking errors |
| [Constraint Violation](#constraint-violation) | `metrics.constraint_violation(...)` | `ConstraintViolationMetricResult` | Boundary distance and violations |
| [Comfort](#comfort) | `metrics.comfort(...)` | `ComfortMetricResult` | Lateral acceleration and jerk |

## Setup

```python
from faran import metrics
from faran.numpy import collectors

state_collector = collectors.states.decorating(planner, transformer=...)
obstacle_collector = collectors.obstacle_states.decorating(observer)

registry = metrics.registry(
    collision_metric := metrics.collision(
        distance_threshold=0.5, distance=distance_extractor,
    ),
    task_metric := metrics.task_completion(
        reference=reference, distance_threshold=2.0,
        time_step_size=0.1, position_extractor=position_extractor,
    ),
    collectors=collectors.registry(state_collector, obstacle_collector),
)
```

## Collision

Evaluates minimum ego–obstacle distances and detects collisions. [`CollisionMetric`](available.md#faran.metrics.collision.CollisionMetric) documents the parameters, and [`CollisionMetricResult`](available.md#faran.metrics.collision.CollisionMetricResult) the result fields.

## Task Completion

Tracks progress along the reference trajectory and goal arrival. [`TaskCompletionMetric`](available.md#faran.metrics.task.TaskCompletionMetric) documents the parameters, and [`TaskCompletionMetricResult`](available.md#faran.metrics.task.TaskCompletionMetricResult) the result fields.

## MPCC Error

Reports contouring and lag errors for [MPCC](../../guide/concepts/mpcc.md) controllers. Requires the cost objects returned by `mppi.mpcc(...)`. [`MpccErrorMetric`](available.md#faran.metrics.error.MpccErrorMetric) documents the parameters, and [`MpccErrorMetricResult`](available.md#faran.metrics.error.MpccErrorMetricResult) the result fields.

## Constraint Violation

Reports boundary distances and flags violations where the vehicle leaves the corridor. [`ConstraintViolationMetric`](available.md#faran.metrics.constraint.ConstraintViolationMetric) documents the parameters, and [`ConstraintViolationMetricResult`](available.md#faran.metrics.constraint.ConstraintViolationMetricResult) the result fields.

## Comfort

Reports lateral acceleration and jerk derived from lateral deviations via finite differences. [`ComfortMetric`](available.md#faran.metrics.comfort.ComfortMetric) documents the parameters, and [`ComfortMetricResult`](available.md#faran.metrics.comfort.ComfortMetricResult) the result fields.

## Live Evaluation

Metrics recompute automatically when new data arrives via collectors:

```python
for step in range(horizon):
    state_collector.step(temperature=50.0, nominal_input=nominal, initial_state=state)
    obstacle_collector.observe(obstacle_states)

    if registry.get(collision_metric).collision_detected:
        break
```
