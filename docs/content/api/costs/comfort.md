---
status: draft
---

# Comfort Costs

## Control Smoothing Cost

Penalizes rate of change between consecutive control inputs[@Liniger2015]. Equation [](#equation-control-smoothing) gives the cost.

/// equation | equation-control-smoothing

$$
J_s = \sum_{d} w_d \, (\mathbf{u}_{t,d} - \mathbf{u}_{t-1,d})^2
$$

- $J_s$ is the smoothing cost at time step $t$.
- $w_d$ is the weight of control dimension $d$.
- $\mathbf{u}_{t,d}$ is control input $d$ at time step $t$.

///

```python
from faran.numpy import costs
import numpy as np

smoothing = costs.comfort.control_smoothing(
    weights=np.array([5.0, 20.0, 5.0]),
)
```

/// backends

::: faran.costs.basic.NumPyControlSmoothingCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.costs.accelerated.JaxControlSmoothingCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

## Control Effort Cost

Penalizes control input magnitudes[@Williams2017]. Equation [](#equation-control-effort) gives the cost.

/// equation | equation-control-effort

$$
J_n = \sum_{d} w_d \, \mathbf{u}_{t,d}^2
$$

- $J_n$ is the effort cost at time step $t$.
- $w_d$ is the weight of control dimension $d$.
- $\mathbf{u}_{t,d}$ is control input $d$ at time step $t$.

///

```python
effort = costs.comfort.control_effort(
    weights=np.array([0.1, 0.5, 0.1]),
)
```

/// backends

::: faran.costs.basic.NumPyControlEffortCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

::: faran.costs.accelerated.JaxControlEffortCost
    options:
      show_root_heading: true
      heading_level: 3
      members:
        - create

///

\bibliography
