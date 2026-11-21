---
status: draft
---

# visualizer

Interactive visualization of simulation results. Distributed as a separate package. For setup and usage, see the [Visualizer guide](../../guide/visualizer.md).

## Installation

```bash
pip install faran-visualizer
```

## Usage

```python
from faran_visualizer import visualizer

mpcc_viz = visualizer.mpcc(
    output="simulation",
    output_directory="./output",
)
```

## Scene

::: faran_visualizer.Scene
    options:
      show_root_heading: true
      heading_level: 3

## render

::: faran_visualizer.render
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - lines
        - dots

## Info

::: faran_visualizer.Info
    options:
      show_root_heading: true
      heading_level: 3

## SimulationVisualizer

::: faran_visualizer.SimulationVisualizer
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - __call__

## MpccSimulationResult

::: faran_visualizer.MpccSimulationResult
    options:
      show_root_heading: true
      heading_level: 3

## MpccVisualizer

::: faran_visualizer.MpccVisualizer
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create
        - __call__
        - scene_of
        - plots_from

## MpccPlots

::: faran_visualizer.MpccPlots
    options:
      show_root_heading: true
      heading_level: 3

## PlotSelection

::: faran_visualizer.PlotSelection
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - __call__

## Plot Types

### Plot

::: faran_visualizer.Plot
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - line

### Plot.Chart

::: faran_visualizer.Plot.Chart
    options:
      show_root_heading: true
      heading_level: 3

### Plot.Line

::: faran_visualizer.Plot.Line
    options:
      show_root_heading: true
      heading_level: 3

### Plot.Band

::: faran_visualizer.Plot.Band
    options:
      show_root_heading: true
      heading_level: 3

### Plot.Bound

::: faran_visualizer.Plot.Bound
    options:
      show_root_heading: true
      heading_level: 3

## Road Network

### Road.Lane

::: faran_visualizer.Road.Lane
    options:
      show_root_heading: true
      heading_level: 3

### Road.Network

::: faran_visualizer.Road.Network
    options:
      show_root_heading: true
      heading_level: 3
