---
hide:
  - navigation
  - toc
water: true
definition: true
---

<faran-stage></faran-stage>

/// hero

# Composable Trajectory Planning for Python

Build trajectory planners from modular components. Set up a working pipeline in minutes, then customize as needed.

[Get Started](guide/getting-started.md){ .faran-button .faran-button--primary }
[Examples](guide/examples/index.md){ .faran-button }
[Repository](https://gitlab.com/risk-metrics/faran){ .faran-button }

///

<div class="faran-home" markdown>

## Why Faran?

/// gallery

### Composable

Swap a cost function, sampler, or dynamics model without touching the rest of your pipeline. If two components can logically work together, they will.

```python
planner, augmented_model, contouring_cost, lag_cost = mppi.mpcc(
    model=model.bicycle.dynamical(...),
    sampler=sampler.halton(
        standard_deviation=[0.5, 0.05], rollout_count=256, knot_count=8, seed=42,
        to_batch=types.bicycle.control_input_batch.create,
    ),
    reference=reference,
    ...
)
```

### Comprehensive

Includes everything for a working planner: dynamics models, samplers, state estimation (KF/EKF/UKF), cost functions, obstacle tracking, risk metrics, and motion prediction.

```python { .faran-imports-shown }
from faran.numpy import (
    mppi,       # planner factories
    model,      # bicycle, unicycle and integrator, with KF, EKF and UKF estimators
    sampler,    # Gaussian and Halton spline samplers
    costs,      # tracking, safety and comfort costs
    risk,       # risk metrics for uncertain obstacles
    obstacles,  # obstacle simulators and observers
    predictor,  # obstacle motion prediction
)
```

### Backend-Agnostic

Set up your planner with NumPy, then switch to JAX by changing one import line. Same API, no code changes. The shared interface makes it possible to add new backends in the future.

```diff
-from faran.numpy import mppi, model, sampler, trajectory, types, extract
+from faran.jax import mppi, model, sampler, trajectory, types, extract
```

### Tested

Extensive test suite for both backends. Full static type checking + runtime shape checking with `jaxtyping` + `beartype`. Misconfigured pipelines fail fast with clear messages.

```python
type StateBatchArray = Float[Array, "T UnicycleD_x M"]
type ControlInputBatchArray = Float[Array, "T UnicycleD_u M"]
```

///

## Quick Start

An [MPCC](guide/concepts/mpcc.md) planner tracking a reference path with a [kinematic bicycle model](api/model/bicycle.md):

```python { .faran-imports-shown }
from faran.numpy import mppi, model, sampler, trajectory, types, extract

reference = trajectory.waypoints(
    points=[(0, 0), (10, 0), (20, 5), (30, 0), (40, -5), (50, 0)],
    path_length=35.0,
)

planner, augmented_model, contouring_cost, lag_cost = mppi.mpcc(
    model=model.bicycle.dynamical(
        time_step_size=0.1, wheelbase=2.5,
        speed_limits=(0.0, 15.0), steering_limits=(-0.5, 0.5),
        acceleration_limits=(-3.0, 3.0),
    ),
    sampler=sampler.gaussian(
        standard_deviation=[0.5, 0.05], rollout_count=256, seed=42,
        to_batch=types.bicycle.control_input_batch.create
    ),
    reference=reference,
    position_extractor=extract.from_physical(lambda states: states.positions),
    config={
        "weights": {"contouring": 100.0, "lag": 100.0, "progress": 1000.0},
        "virtual": {"velocity_limits": (0.0, 15.0)},
    },
)
```

To use JAX, change `from faran.numpy` to `from faran.jax`. Everything else can stay the same.

[Full walkthrough](guide/getting-started.md){ .md-button }

## Explore the Docs

/// docs-map

- [Getting Started](guide/getting-started.md): Install Faran, build your first planner, and run a simulation loop.
- [User Guide](guide/concepts/index.md): See the math behind the algorithms and understand how the components work together.
- [Examples](guide/examples/index.md): End-to-end scenarios with interactive visualizations of path following, boundaries and obstacle avoidance.
- [API Reference](api/index.md): Detailed usage instructions for every component.
- [Gotchas & FAQ](guide/concepts/gotchas.md): Known limitations, common pitfalls, and workarounds.

Point at a section, and Faran's MPPI planner, running in your browser with Pyodide, finds a path to it.

///

## Backends

/// columns

Faran is designed to let you focus on your research and worry less about performance optimizations. All current and future backends are guaranteed to share the same API, so you can prototype with any backend now and switch to a faster one later (see [Backend Architecture](guide/backends.md) for details). Currently the following backends are available:

| Backend   | Import                        | Best for                                                |
|-----------|-------------------------------|---------------------------------------------------------|
| **NumPy** | `from faran.numpy import ...` | Prototyping, debugging, parameter sweeps                |
| **JAX**   | `from faran.jax import ...`   | Performance, GPU acceleration, large-scale computations |

Of course, if you implement your own custom components, they might be tied to a specific backend, so there's unfortunately no magic there.

---

//// variants | Backend

///// variant | NumPy
    note: Prototyping and debugging

```python { .faran-imports-shown hl_lines="1" }
from faran.numpy import mppi, model, sampler, trajectory, types, extract

reference = trajectory.waypoints(
    points=[(0, 0), (10, 0), (20, 5), (30, 0), (40, -5), (50, 0)],
    path_length=35.0,
)

planner, augmented_model, contouring_cost, lag_cost = mppi.mpcc(
    model=model.bicycle.dynamical(time_step_size=0.1, wheelbase=2.5, ...),
    sampler=sampler.gaussian(standard_deviation=[0.5, 0.05], rollout_count=256, ...),
    reference=reference,
    ...
)
```

/////

///// variant | JAX
    note: Compiled, can run on the GPU

```python { .faran-imports-shown hl_lines="1" }
from faran.jax import mppi, model, sampler, trajectory, types, extract

reference = trajectory.waypoints(
    points=[(0, 0), (10, 0), (20, 5), (30, 0), (40, -5), (50, 0)],
    path_length=35.0,
)

planner, augmented_model, contouring_cost, lag_cost = mppi.mpcc(
    model=model.bicycle.dynamical(time_step_size=0.1, wheelbase=2.5, ...),
    sampler=sampler.gaussian(standard_deviation=[0.5, 0.05], rollout_count=256, ...),
    reference=reference,
    ...
)
```

/////

////

Only the highlighted import line changes. The planner, its components and their arguments stay the same.

///

!!! info "Under Active Development"

    Faran is being actively developed. That means some features may be missing, there are [some gotchas](guide/concepts/gotchas.md), and some of the API might change. See the [feature overview](guide/features.md) for what's available and what's coming.

<div class="acknowledgements" markdown>

**Acknowledgements** · Logo designed with input from [Ilia Valian](https://www.linkedin.com/in/ilia-valian/).

</div>

</div>
