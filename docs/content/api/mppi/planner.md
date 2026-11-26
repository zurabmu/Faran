---
status: draft
---

# Planner Factories

Factory functions and concrete classes for the [MPPI](index.md) planner. See the [parent page](index.md) for the algorithm description, equations, and configuration-level overview.

/// backends

::: faran.mppi.basic.NumPyMppi
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create
        - step

::: faran.mppi.accelerated.JaxMppi
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create
        - step

///

## MPCC Factory

/// backends

::: faran.mpcc.basic.NumPyMpccMppi
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.mpcc.accelerated.JaxMpccMppi
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Augmented Factory

/// backends

::: faran.states.augmented.mppi.basic.NumPyAugmentedMppi
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.states.augmented.mppi.accelerated.JaxAugmentedMppi
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## MPCC Configuration

/// backends

::: faran.mpcc.basic.NumPyMpccWeightConfig
    options:
      show_root_heading: true
      heading_level: 3
      members: false

::: faran.mpcc.accelerated.JaxMpccWeightConfig
    options:
      show_root_heading: true
      heading_level: 3
      members: false

///

/// backends

::: faran.mpcc.basic.NumPyMpccVirtualStateConfig
    options:
      show_root_heading: true
      heading_level: 3
      members: false

::: faran.mpcc.accelerated.JaxMpccVirtualStateConfig
    options:
      show_root_heading: true
      heading_level: 3
      members: false

///

## Supporting Types

### Control

The return type of `planner.step()`.

::: faran.types.Control
    options:
      show_root_heading: true
      heading_level: 4

### Update Functions

::: faran.mppi.common.UseOptimalControlUpdate
    options:
      show_root_heading: true
      heading_level: 4

::: faran.mppi.common.NoFilter
    options:
      show_root_heading: true
      heading_level: 4
