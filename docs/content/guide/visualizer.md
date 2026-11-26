---
status: draft
---

# Visualizer

`faran-visualizer` can generate visualizations from the simulation results. It contains, among other things, visualizations of the planned trajectories, reference paths, obstacle trajectories, and can show configurable time series plots for other metrics.

## Installation

```bash
pip install faran-visualizer[rerun]
```

The `rerun` extra installs the Rerun viewer. Without it, only the canvas renderer works (see [Renderers](#renderers)). If you want to show visualizations in Jupyter notebooks as well, install `faran-visualizer[notebook]` instead.

In order to view a visualization, you need to open it in the same version of `faran-visualizer` that was used to create it.

## How It Works

1. You describe what to show as a `Scene`: renderings in the x-y plane, plots over time, and an info table. For MPCC simulations, `MpccSimulationResult` builds the scene for you.
2. You call a visualizer factory (e.g. `visualizer.simulation()` or `visualizer.mpcc()`) to create a visualizer.
3. The visualizer creates a visualization from the scene.

The output will be in the configured directory (default: `visualizations` in the current working directory), as a `<key>.json` file with the default renderer. You can open it in the browser with `faran-visualizer view <key>.json`. In a Jupyter notebook, `faran_visualizer.show("<key>.json")` shows it in the cell output.

```python
from faran_visualizer import configure
configure(output_directory="./results")
```

## Renderers

A renderer saves the visualization and opens it again. There are two:

| Renderer | Saves | Opens it in |
|----------|-------|-------------|
| `CanvasRenderer()` (default) | `<key>.json` | A page in your browser, drawn by the canvas engine that this site also uses |
| `RerunRenderer()` | `<key>.frn` | The Rerun viewer, which needs the `rerun` extra. `faran-visualizer view --browser` opens the Rerun web viewer instead |

Set the renderer for every visualizer with `configure`, or for one visualizer with its factory:

```python
from faran_visualizer import RerunRenderer, configure, visualizer

configure(output_directory="./results", renderer=RerunRenderer())
visualize = visualizer.mpcc(renderer=RerunRenderer())
```

`faran-visualizer view` and `faran_visualizer.show` pick the renderer from the file's extension, so both kinds of files open the same way. The canvas renderer needs no packages beyond the visualizer's own, so it also works in [Pyodide](https://pyodide.org).

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

The fields of [`MpccSimulationResult`](../api/visualizer/index.md#faran_visualizer.MpccSimulationResult) say what each one renders and which ones are required.

## Generic Visualization

For any other simulation, describe what to show as a `Scene`. The renderings come from the `render` namespace. `background` holds the renderings shown at every step, and `at_step` returns the renderings of one step. Every step must return renderings with the same names, in the same order. The name of a rendering is also its name in the viewer. The label of a rendering is its entry in the legend, and renderings with the same label, such as a plan and its points, share one entry.

```python
import asyncio
from faran_visualizer import Info, Plot, Scene, render, visualizer

scene = Scene(
    time_step=0.05,
    step_count=len(positions),
    background=[
        render.dots(name="waypoints", label="Waypoints", positions=waypoints, color="#457b9d", size=6.0),
    ],
    at_step=lambda step: [
        render.lines(name="drone/path", label="Traveled path", strips=[positions[: step + 1]], color="#e63946"),
        render.lines(name="drone/plan", label="Plan", strips=[plans[step]], color="#e63946", pattern="dashed"),
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
