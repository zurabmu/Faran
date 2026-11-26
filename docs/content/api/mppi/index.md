---
status: draft
---

# mppi

MPPI (Model Predictive Path Integral) is a sampling-based [MPC](../../guide/concepts/mpc.md) algorithm for trajectory planning[@Williams2015][@Williams2016]. For background on trajectory planning and MPC, see the [guide](../../guide/concepts/planning.md).

## Algorithm

Given a dynamical model $f$, cost function $\mathbf{J}$, sampling distribution $\boldsymbol{\mathcal{Z}}$, time horizon $T$, rollout count $M$, planning period $P$, and temperature $\lambda$:

1. Sample $M$ control perturbations around the nominal sequence: $\mathbf{u}_m = \text{sample}(\mathbf{u}, \boldsymbol{\mathcal{Z}})$
2. Simulate each through the dynamics: $\mathbf{x}_m = \text{simulate}(\mathbf{u}_m, \mathsf{x}_0, f)$
3. Evaluate costs: $\mathbf{J}_m = \mathbf{J}(\mathbf{u}_m, \mathbf{x}_m)$
4. Compute the softmax weights with equation [](#equation-mppi-weights) and the optimal control as their weighted average with equation [](#equation-mppi-control).

/// equation | equation-mppi-weights

$$
w_m = \frac{1}{\eta} \exp\!\left(-\frac{1}{\lambda}(\mathbf{J}_m - \mathbf{J}_{\min})\right), \quad \eta = \sum_{m=1}^{M} \exp\!\left(-\frac{1}{\lambda}(\mathbf{J}_m - \mathbf{J}_{\min})\right)
$$

- $w_m$ is the importance weight of rollout $m$.
- $\mathbf{J}_m$ is the cost of rollout $m$.
- $\mathbf{J}_{\min}$ is the minimum cost across all rollouts.
- $\lambda$ is the temperature, which sets how strongly the weights favor low-cost rollouts.
- $\eta$ is the normalization constant.

///

/// equation | equation-mppi-control

$$
\mathbf{u}_{\text{opt}} = \text{filter}\!\left(\sum_{m=1}^{M} w_m \, \mathbf{u}_m\right)
$$

- $\mathbf{u}_{\text{opt}}$ is the optimal control sequence.
- $\mathbf{u}_m$ is the control sequence of rollout $m$.
- $\text{filter}$ is the [filter](filter.md) applied to the weighted average.

///

After computing $\mathbf{u}_{\text{opt}}$, the nominal sequence is updated, the first $P$ actions are executed, and the sequence is shifted forward with zero-padding.

## Configuration Levels

Three factory functions provide increasing levels of abstraction.

### `mppi.base`

Assembles a planner from a [model](../model/index.md), [cost function](../costs/index.md), and [sampler](../sampler/index.md). [`NumPyMppi.create`](planner.md#faran.mppi.basic.NumPyMppi.create) documents its parameters.

```python
from faran.numpy import mppi, model, sampler, costs, types
import numpy as np

planner = mppi.base(
    model=model.bicycle.dynamical(time_step_size=0.1, wheelbase=2.5),
    cost_function=costs.combined(...),
    sampler=sampler.gaussian(
        standard_deviation=np.array([0.5, 0.05]),
        rollout_count=256,
        to_batch=types.bicycle.control_input_batch.create,
        seed=42,
    ),
)
```

### `mppi.augmented`

Composes separate physical and virtual models into a single augmented planner. Used when the state space needs extension (e.g. adding a path parameter for [MPCC](../../guide/concepts/mpcc.md)). [`NumPyAugmentedMppi.create`](planner.md#faran.states.augmented.mppi.basic.NumPyAugmentedMppi.create) documents its parameters.

```python
from faran.numpy import mppi, model, sampler, costs, types
import numpy as np

setup = mppi.augmented(
    models=(physical_model, virtual_model),
    samplers=(physical_sampler, virtual_sampler),
    cost=costs.combined(...),
    state=types.augmented.state,
    state_sequence=types.augmented.state_sequence,
    state_batch=types.augmented.state_batch,
    input_batch=types.augmented.control_input_batch,
)
planner = setup.mppi
```

### `mppi.mpcc`

Highest-level factory for [MPCC](../../guide/concepts/mpcc.md) path following. Automatically constructs the augmented state space with a virtual path parameter $\phi$, and configures [contouring, lag, and progress costs](../costs/tracking.md).

Returns a `NamedTuple` of `(mppi, model, contouring_cost, lag_cost)`. [`NumPyMpccMppi.create`](planner.md#faran.mpcc.basic.NumPyMpccMppi.create) documents its parameters.

```python
from faran.numpy import mppi, model, sampler, costs, types, extract, filters
from numtypes import array

planner, augmented_model, contouring_cost, lag_cost = mppi.mpcc(
    model=model.bicycle.dynamical(
        time_step_size=0.1, wheelbase=2.5,
        speed_limits=(0.0, 15.0), steering_limits=(-0.5, 0.5),
        acceleration_limits=(-3.0, 3.0),
    ),
    sampler=sampler.gaussian(
        standard_deviation=array([0.5, 0.2], shape=(2,)),
        rollout_count=256,
        to_batch=types.bicycle.control_input_batch.create,
        seed=42,
    ),
    costs=(
        costs.comfort.control_smoothing(weights=array([5.0, 20.0, 5.0], shape=(3,))),
    ),
    reference=reference,
    position_extractor=extract.from_physical(lambda states: states.positions),
    config={
        "weights": {"contouring": 50.0, "lag": 100.0, "progress": 1000.0},
        "virtual": {"velocity_limits": (0.0, 15.0)},
    },
    filter_function=filters.savgol(window_length=11, polynomial_order=3),
)
```

#### MPCC Configuration Defaults

The `config` dict is deep-merged with the defaults that [`NumPyMpccWeightConfig`](planner.md#faran.mpcc.basic.NumPyMpccWeightConfig) and [`NumPyMpccVirtualStateConfig`](planner.md#faran.mpcc.basic.NumPyMpccVirtualStateConfig) list.

## Planning Loop

```python
state = initial_state
nominal = initial_nominal_input

for step in range(max_steps):
    control = planner.step(
        temperature=50.0, nominal_input=nominal, initial_state=state,
    )
    state = dynamics.step(inputs=control.optimal, state=state)
    nominal = control.nominal
```

`planner.step()` returns a [`Control`](planner.md#faran.types.Control) with the optimal and the nominal control sequence and the rollout weights.

## Mppi Protocol

::: faran.types.Mppi
    options:
      show_root_heading: true
      heading_level: 3

\bibliography
