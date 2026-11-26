---
status: draft
---

# Single Integrator Model

$D$-dimensional single integrator where each state is driven directly by a velocity input, as equation [](#equation-integrator) shows.

/// equation | equation-integrator

$$
\mathbf{x}_{t+1} = \operatorname{clip}\!\bigl(\mathbf{x}_t + \operatorname{clip}(\mathbf{u}_t,\; v_{\min}, v_{\max}) \cdot \Delta t,\; s_{\min}, s_{\max}\bigr)
$$

- $\mathbf{x}_t$ is the state at time step $t$.
- $\mathbf{u}_t$ is the velocity input.
- $v_{\min}$ and $v_{\max}$ are the velocity limits.
- $s_{\min}$ and $s_{\max}$ are the state limits.
- $\Delta t$ is the time step size.

///

The state $\mathbf{x} \in \mathbb{R}^{D}$ is a position of arbitrary dimension, and the control input $\mathbf{u} \in \mathbb{R}^{D}$ is its velocity. When `periodic=True`, the state wraps around at the limits instead of clamping. Used internally for the MPCC virtual state (path parameter $\phi$); see [MPCC configuration](../mppi/index.md).

```python
from faran.numpy import model

integrator = model.integrator.dynamical(
    time_step_size=0.1,
    velocity_limits=(0.0, 15.0),
    periodic=False,
)
```

/// backends

::: faran.models.integrator.basic.NumPyIntegratorModel
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

::: faran.models.integrator.accelerated.JaxIntegratorModel
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

///
