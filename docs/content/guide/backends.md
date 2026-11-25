---
status: draft
---

# Backends

Faran exposes compatible APIs for two backends. You can switch by changing the import statements:

```python
# NumPy — prototyping, debugging
from faran.numpy import mppi, model, sampler, costs, trajectory, boundary, types

# JAX — GPU acceleration, JIT compilation
from faran.jax import mppi, model, sampler, costs, trajectory, boundary, types
```

Compatible means that all backends speak the language of NumPy. That means NumPy arrays can be used for configuration everywhere, and all outputs can be converted to NumPy arrays with `np.asarray()` (see [Output Conversion](#output-conversion)). Also, all backends support the API that the NumPy backend defines, but specific backends may have additional features.

## Consistency

All components in a pipeline must use the same backend. Mixing `faran.numpy` and `faran.jax` objects will produce errors.

## Output Conversion

All results or inputs can be converted to NumPy arrays via `np.asarray()`:

```python
import numpy as np

numpy_array = np.asarray(jax_control.optimal)
```

This is convenient if you want to serialize data, perform computations that are not performance-sensitive, or whatever else you might use NumPy for.

## Compiling Your Own Functions

<!-- TODO: Explain when you would compile your own function over JAX components, and that JAX planners already compile each planning step without this. -->

```python
from flax import nnx
from faran.jax import obstacles, predictor, register, types

provider = obstacles.provider.predicting(
    predictor=predictor.static(horizon=10),
    history=types.obstacle_states_running_history.empty(
        creator=types.obstacle_2d_poses, horizon=1, obstacle_count=2
    ),
)
register(provider)


@nnx.jit
def forecast(provider):
    return provider()


provider.observe(observation)
forecast(provider)  # Predicts from the latest observation.
```

<!-- TODO: Explain the two requirements: register the component (and everything it references) with `register`, and pass it to the compiled function as an argument. Mention that state, such as the provider's history or a sampler's random key, carries over from one call to the next. -->

### `UntracedStateError`

<!-- TODO: Explain what the error means: a compiled function read the state of a component that it does not receive as an argument, for example through a closure, so the compiled function would keep using the value it saw when it was first compiled. -->

```python
@nnx.jit
def forecast_from_closure():
    return provider()  # Raises UntracedStateError.


@nnx.jit
def forecast(provider):
    return provider()  # Works: the provider is an argument.
```

### Components with State

<!-- TODO: Explain how to write your own component with state: declare the field as `pytree.Variable[T]`, create it with `pytree.variable(value)`, and read and write it with `get()` and `set()`. -->

```python
from dataclasses import dataclass
from faran import pytree

import jax


@dataclass(frozen=True)
class Counter:
    count: pytree.Variable[jax.Array]

    @staticmethod
    def create() -> "Counter":
        return Counter(count=pytree.variable(jax.numpy.array(0)))

    def increment(self) -> jax.Array:
        self.count.set(self.count.get() + 1)
        return self.count.get()
```
