---
status: draft
---

# Risk Metrics

Risk metrics aggregate sampled collision costs into a single scalar that emphasizes dangerous tail outcomes[@Majumdar2020]. Passed to [collision cost](safety.md#collision-cost) via the `metric` parameter.

## Available Metrics

Each metric reduces the sampled collision costs $J$ of a rollout to one value. The obstacle pose sampler draws `sample_count` samples per rollout.

### Expected Value

Risk-neutral baseline, given by equation [](#equation-expected-value). Equivalent to no risk metric.

/// equation | equation-expected-value

$$
\rho(J) = \mathbb{E}[J]
$$

- $\rho$ is the risk of the sampled costs.
- $J$ is the sampled collision cost.

///

```python
from faran.numpy import risk

metric = risk.expected_value(sample_count=50)
```

### Mean-Variance

Adds the variance of the sampled costs to their mean, as in mean-variance portfolio selection[@Markowitz1952]. With $\gamma = 0$, equation [](#equation-mean-variance) reduces to the expected value, and $\gamma > 0$ penalizes cost variability.

/// equation | equation-mean-variance

$$
\rho(J) = \mathbb{E}[J] + \gamma \, \operatorname{Var}[J]
$$

- $\gamma$ is the variance weight, `gamma`.

///

```python
metric = risk.mean_variance(gamma=1.0, sample_count=50)
```

### Value at Risk

The $\alpha$-quantile of the cost distribution[@Duffie1997], as equation [](#equation-value-at-risk) defines it.

/// equation | equation-value-at-risk

$$
\operatorname{VaR}_\alpha(J) = \inf\{c : P(J \leq c) \geq \alpha\}
$$

- $\alpha$ is the confidence level, `alpha`.
- $c$ is a cost threshold.

///

```python
metric = risk.var(alpha=0.95, sample_count=50)
```

### Conditional Value at Risk

The expected cost in the worst $(1 - \alpha)$ fraction of samples[@Rockafellar2000], as equation [](#equation-conditional-value-at-risk) defines it. CVaR satisfies the axioms that Majumdar and Pavone propose for assessing risk in robotics[@Majumdar2020], and it has been used with MPPI for obstacle avoidance[@Yin2023], which makes it a good default for safety-critical planning.

/// equation | equation-conditional-value-at-risk

$$
\operatorname{CVaR}_\alpha(J) = \mathbb{E}\bigl[J \mid J \geq \operatorname{VaR}_\alpha(J)\bigr]
$$

- $\operatorname{VaR}_\alpha$ is the value at risk from equation [](#equation-value-at-risk).
- $\alpha$ is the confidence level, `alpha`.

///

```python
metric = risk.cvar(alpha=0.95, sample_count=50)
```

### Entropic Risk

The entropic risk measure[@Follmer2002] in equation [](#equation-entropic-risk). A positive $\theta$ makes the metric risk-averse, and a larger $\theta$ gives more weight to the tail of the cost distribution.

/// equation | equation-entropic-risk

$$
\rho_\theta(J) = \frac{1}{\theta}\ln\!\bigl(\mathbb{E}[e^{\theta J}]\bigr)
$$

- $\theta$ is the risk aversion, `theta`.

///

```python
metric = risk.entropic_risk(theta=1.0, sample_count=50)
```

### No Metric

Deterministic single-sample evaluation. Used when `metric` is omitted from the collision cost.

```python
metric = risk.none()
```

## Usage

```python
from faran.numpy import costs, risk
import numpy as np

collision = costs.safety.collision(
    obstacle_states=provider,
    sampler=obstacle_sampler,
    distance=distance_extractor,
    distance_threshold=np.array([0.5, 0.5, 0.5]),
    weight=1500.0,
    metric=risk.cvar(alpha=0.95, sample_count=50),
)
```

::: faran.costs.risk.base.RisKitRiskMetric
    options:
      show_root_heading: true
      heading_level: 2
      members:
        - create

\bibliography
