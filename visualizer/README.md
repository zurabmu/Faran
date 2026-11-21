# faran-visualizer

Interactive visualization tool for [faran](https://gitlab.com/risk-metrics/faran) trajectory planning simulations.

## Installation

```bash
pip install faran-visualizer
```

Or with uv:

```bash
uv add faran-visualizer
```

## Requirements

- **Python 3.13+**

## Usage

### Basic Usage

```python
from faran_visualizer import visualizer, MpccSimulationResult

# Create a visualizer instance
mpcc_viz = visualizer.mpcc()

# After running your simulation, create a result object
result = MpccSimulationResult(
    reference=trajectory,
    states=states,
    optimal_trajectories=optimal_trajectories,
    nominal_trajectories=nominal_trajectories,
    contouring_errors=contouring_errors,
    lag_errors=lag_errors,
    wheelbase=wheelbase,
    max_contouring_error=max_contouring_error,
    max_lag_error=max_lag_error,
)

# Create the visualization
await mpcc_viz(result, key="my-simulation")
```

## Output

The visualization is saved as `<key>.frn`, which you can open with:

```bash
faran-visualizer view visualizations/mpcc-simulation/my-simulation.frn            # viewer
faran-visualizer view visualizations/mpcc-simulation/my-simulation.frn --browser  # browser
```
