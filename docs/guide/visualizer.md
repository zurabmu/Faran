---
status: draft
---

# Visualizer

`faran-visualizer` can generate visualizations from the simulation results. It contains, among other things, visualizations of the planned trajectories, reference paths, obstacle trajectories, and can show configurable time series plots for other metrics.

## Installation

```bash
pip install faran-visualizer
```

If you want to show visualizations in Jupyter notebooks as well, install `faran-visualizer[notebook]` instead.

In order to view a visualization, you need to open it in the same version of `faran-visualizer` that was used to create it.

## How It Works

1. You describe what to show as a `Scene`: renderings in the x-y plane, plots over time, and an info table. For MPCC simulations, `MpccSimulationResult` builds the scene for you.
2. You call a visualizer factory (e.g. `visualizer.simulation()` or `visualizer.mpcc()`) to create a visualizer.
3. The visualizer creates a visualization from the scene.

The output will be in the configured directory (default: `visualizations` in the current working directory), as a `<key>.frn` file. You can view it in the viewer with `faran-visualizer view <key>.frn`, or in the browser with `faran-visualizer view <key>.frn --browser`. In a Jupyter notebook, `faran_visualizer.show("<key>.frn")` shows it in the cell output.

```python
from faran_visualizer import configure
configure(output_directory="./results")
```

## MPCC Visualization

For planners created with `mppi.mpcc()`, use `MpccSimulationResult` for convenience:

```python
import asyncio
from faran_visualizer import visualizer, MpccSimulationResult, configure

result = MpccSimulationResult(
    reference=reference,
    states=collected_states,
    contouring_errors=errors.contouring,
    lag_errors=errors.lag,
    time_step_size=0.1,
    wheelbase=2.5,
)

configure(output_directory=".")
asyncio.run(visualizer.mpcc()(result, key="my-simulation"))
```

### Required Fields

| Field               | Type            | Description                                 |
|---------------------|-----------------|---------------------------------------------|
| `reference`         | `Trajectory`    | The reference path used by MPCC             |
| `states`            | `StateSequence` | Augmented state history from collectors     |
| `contouring_errors` | `array`         | Contouring errors from `metrics.mpcc_error` |
| `lag_errors`        | `array`         | Lag errors from `metrics.mpcc_error`        |
| `time_step_size`    | `float`         | Simulation time step (seconds)              |
| `wheelbase`         | `float`         | Length of the rendered boxes (meters)          |

### Optional Fields

| Field                  | Description                                                        |
|------------------------|--------------------------------------------------------------------|
| `obstacles`            | Obstacle state history for rendering obstacles                     |
| `obstacle_forecasts`   | Predicted obstacle trajectories                                    |
| `boundary`             | Corridor boundary to render                                          |
| `controls`             | Control input history                                              |
| `risks`                | Risk metric values over time                                       |
| `optimal_trajectories` | Best trajectory at each step                                       |
| `nominal_trajectories` | Nominal (warm-started) trajectory at each step                     |
| `vehicle_width`        | Width of the rendered boxes (meters), required when boxes are rendered   |
| `vehicle_type`         | `"car"` or `"triangle"` renders the ego as a box, `"circle"` as a circle |
| `vehicle_radius`       | Radius of the ego when rendered as a circle (meters)                  |
| `obstacle_shape`       | `"rectangle"` renders obstacles as boxes, `"circle"` as circles      |
| `obstacle_radius`      | Radius of obstacles when rendered as circles (meters)                 |
| `max_contouring_error` | TODO                                                               |
| `max_lag_error`        | TODO                                                               |
| `network`              | Lanes to render, as a `Road.Network`                                 |
| `plots`                | TODO, see [Custom Plots](#custom-plots)                            |

## Generic Visualization

For any other simulation, describe what to show as a `Scene`. The renderings come from the `render` namespace. `background` holds the renderings shown at every step, and `at_step` returns the renderings of one step. Every step must return renderings with the same names, in the same order. The name of a rendering is also its name in the viewer.

```python
import asyncio
from faran_visualizer import Info, Plot, Scene, render, visualizer

scene = Scene(
    time_step=0.05,
    step_count=len(positions),
    background=[
        render.dots(name="waypoints", positions=waypoints, color="#457b9d", size=6.0),
    ],
    at_step=lambda step: [
        render.lines(name="drone/path", strips=[positions[: step + 1]], color="#e63946"),
        render.lines(name="drone/plan", strips=[plans[step]], color="#e63946", pattern="dashed"),
    ],
    plots=[Plot.line(name="Thrust", values=thrust, unit="N")],
    info=[Info(label="Altitude", values=altitudes, unit="m")],
)

asyncio.run(visualizer.simulation()(scene, key="my-simulation"))
```

Colors are hex colors such as `"#3498db"` or `"#3498db80"`, or basic color names such as `"red"`.

## Custom Plots

Attach additional time-series plots with optional bounds and uncertainty bands:

```python
from faran_visualizer import Plot

scene = Scene(
    ...,
    plots=[
        speed := Plot.line(name="Speed", values=speeds, unit="m/s"),
        risk := Plot(
            name="Risk",
            scale="log",
            lines=[
                Plot.Line(label="Selected", values=selected, color="red"),
                Plot.Line(label="Median", values=median),
            ],
            bands=[Plot.Band(label="10-90%", lower=low, upper=high)],
            bounds=[Plot.Bound(label="Limit", values=1.0)],
        ),
    ],
)
```

TODO: `Plot.line`, `Plot.Bound`.

TODO: `Plot.Chart`.

```python
plots = [
    errors := Plot.Chart(
        name="Tracking Errors",
        unit="m",
        plots=[
            contouring := Plot.line(name="Contouring Error", values=contouring_errors),
            lag := Plot.line(name="Lag Error", values=lag_errors),
        ],
    ),
]
```

TODO: MPCC plots (`plots_from`, `MpccPlots`, overriding and extending with `create(plots=...)`, `PlotSelection`).

```python
from dataclasses import replace
from faran_visualizer import MpccVisualizer

renamed = MpccVisualizer.create(
    plots=lambda plots, result: [
        plots.progress,
        replace(plots.tracking_errors, name="Errors"),
    ]
)
extended = MpccVisualizer.create(
    plots=lambda plots, result: [
        *plots.all,
        Plot.line(name="Speed", values=speed_of(result.states)),
    ]
)
```

For API signatures and detailed options, see the [Visualizer API reference](../api/visualizer/index.md).
