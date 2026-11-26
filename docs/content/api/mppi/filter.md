---
status: draft
---

# Filters

Filters post-process the weighted-average optimal control sequence produced by the [MPPI](index.md) planner. They correspond to the $\text{filter}(\cdot)$ operation in the MPPI algorithm.

## Savitzky-Golay Filter

Fits a low-degree polynomial to successive windows of the optimal control sequence via least squares[@Savitzky1964][@Williams2018], then takes the fitted value at each window center as the smoothed output. Applied independently to each control dimension.

Given a half-window size $w$ and polynomial degree $p$ (with $p < 2w + 1$), equation [](#equation-savitzky-golay) gives the smoothed value at time step $t$.

/// equation | equation-savitzky-golay

$$
\hat{y}_t = \sum_{j=-w}^{w} c_j \, y_{t+j}
$$

- $\hat{y}_t$ is the smoothed value at time step $t$.
- $y_{t+j}$ is the unsmoothed value at time step $t + j$.
- $c_j$ are the convolution coefficients, which depend only on $w$ and $p$ and are computed once.

///

/// live | Savitzky-Golay filter

```python
--8<-- "docs/snippets/savgol.py"
```

///

Pass the filter to any [MPPI factory](index.md) as `filter_function`.

/// backends

::: faran.mppi.savgol.basic.NumPySavGolFilter
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.mppi.savgol.accelerated.JaxSavGolFilter
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## No Filter

Identity filter — returns the optimal input unchanged. This is the default when no `filter_function` is provided.

::: faran.mppi.common.NoFilter
    options:
      show_root_heading: true
      heading_level: 3

\bibliography
