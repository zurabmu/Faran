try:
    from beartype import beartype  # pyright: ignore[reportMissingImports]

    typechecker = beartype
except ImportError:
    typechecker = None

from dataclasses import Field, dataclass, field
from typing import Literal, Protocol, Any, Callable, Final, runtime_checkable

from numpy.typing import NDArray
from jaxtyping import jaxtyped as jaxtyping_jaxtyped, Array as JaxArray
from jax.tree_util import register_dataclass
from jax.core import Tracer
from flax import nnx

import jax
import numpy as np
import jax.numpy as jnp

type Array = NDArray
type DataType = np.dtype
type Device = Literal["cpu", "default"]

_STATIC: Final = {"static": True}


@runtime_checkable
class ArrayConvertible(Protocol):
    def __array__(self, dtype: DataType | None = None) -> Array:
        """Returns an array representation of the object, optionally with the specified dtype."""
        ...


@runtime_checkable
class HasShape(Protocol):
    @property
    def shape(self) -> tuple[int, ...]:
        """Returns the shape of the array-like object."""
        ...


jaxtyped = jaxtyping_jaxtyped(typechecker=typechecker)
"""Wrapper around `jaxtyping.jaxtyped` that conditionally applies type checking."""


class pytree:
    @staticmethod
    def __new__[T](cls, target: type[T]) -> type[T]:
        """Registers a dataclass as a JAX pytree."""
        return register_dataclass(target)

    @staticmethod
    def static_field[T](*, default_factory: Callable[[], T] | None = None) -> Any:
        """Declares a dataclass field that JAX does not trace."""
        if default_factory is None:
            return field(metadata=_STATIC)

        return field(default_factory=default_factory, metadata=_STATIC)

    @staticmethod
    def is_static(field: Field[Any]) -> bool:
        """Returns true when a dataclass field was declared with `static_field`."""
        return field.metadata == _STATIC


@dataclass(frozen=True)
class Variable[T]:
    """A value that a compiled planner step can replace. The step's last value is kept for the
    next step.
    """

    _cell: nnx.Variable[T]

    @staticmethod
    def create[V](value: V) -> "Variable[V]":
        return Variable(nnx.Variable(value))

    def get(self) -> T:
        value = self._cell.get_value()

        if not is_traced(value) and is_inside_trace():
            raise UntracedStateError(
                "The state of a component was read inside a compiled function that does not "
                "receive the state as an input, so the compiled function would not see the latest "
                "value of the state. Register the component with `faran.jax.register` and pass it "
                "as an argument to a function compiled with `nnx.jit`."
            )

        return value

    def set(self, value: T) -> None:
        self._cell.set_value(value)


class UntracedStateError(Exception):
    """Raised when the state of a component is read inside a compiled function that does not
    receive the state as an input.
    """

    ...


def is_traced(value: Any) -> bool:
    return all(isinstance(leaf, Tracer) for leaf in jax.tree.leaves(value))


def is_inside_trace() -> bool:
    # NOTE: JAX has no public function that reports whether it is tracing. Inside a trace,
    # every new array is a tracer.
    return isinstance(jnp.zeros(()), Tracer)


def place(array: Array | JaxArray, *, device: Device) -> JaxArray:
    """Place an array on the specified device.

    Args:
        array: The array to place.
        device: The device to place the array on. Can be "cpu" or "default".

    Returns:
        The array placed on the specified device.
    """
    match device:
        case "cpu":
            return jnp.asarray(array, device=jax.devices("cpu")[0])
        case "default":
            return jnp.asarray(array)
        case _:
            raise ValueError(f"Unsupported device: {device}")
