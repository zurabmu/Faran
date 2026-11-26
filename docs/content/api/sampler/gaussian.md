---
status: draft
---

# Gaussian Sampler

i.i.d. zero-mean Gaussian perturbations per timestep, the sampling distribution of the original MPPI[@Williams2017], distributed as equation [](#equation-gaussian-perturbation) shows.

/// equation | equation-gaussian-perturbation

$$
\boldsymbol{\epsilon}_t^{(m)} \sim \mathcal{N}(\mathbf{0},\, \operatorname{diag}(\boldsymbol{\sigma}^2))
$$

- $\boldsymbol{\epsilon}_t^{(m)}$ is the perturbation of rollout $m$ at time step $t$.
- $\boldsymbol{\sigma}$ is the per-dimension standard deviation.

///

/// live | Gaussian rollouts
    still: true

```python
--8<-- "docs/snippets/gaussian.py"
```

///

/// backends

::: faran.samplers.gaussian.basic.NumPyGaussianSampler
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

::: faran.samplers.gaussian.accelerated.JaxGaussianSampler
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

///

\bibliography
