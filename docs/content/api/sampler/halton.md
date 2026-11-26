---
status: draft
---

# Halton Spline Sampler

Quasi-random perturbations with temporal smoothness[@Halton1960]. Halton sequences in $D_u \times K$ dimensions produce low-discrepancy uniform samples, transformed to Gaussian via the inverse normal CDF, then interpolated across the time horizon with natural cubic splines, similar to the sampling in STORM[@Bhardwaj2022].

Maximum Halton dimension: $D_u \times K \leq 180$ (JAX backend).

/// live | Halton spline rollouts
    still: true

```python
--8<-- "docs/snippets/halton.py"
```

///

/// backends

::: faran.samplers.halton.basic.NumPyHaltonSplineSampler
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

::: faran.samplers.halton.accelerated.JaxHaltonSplineSampler
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

///

\bibliography
