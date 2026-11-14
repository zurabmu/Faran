try:
    from beartype import beartype  # pyright: ignore[reportMissingImports]

    typechecker = beartype
except ImportError:
    typechecker = None

from dataclasses import field
from typing import Literal, Protocol, Any, runtime_checkable

from numpy.typing import NDArray
from jaxtyping import jaxtyped as jaxtyping_jaxtyped, Array as JaxArray
from jax.tree_util import register_dataclass

import jax
import numpy as np
import jax.numpy as jnp

type Array = NDArray
type DataType = np.dtype
type Device = Literal["cpu", "default"]


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
    def static_field() -> Any:
        """Declares a dataclass field that JAX does not trace. Its value must be hashable."""
        return field(metadata={"static": True})


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
