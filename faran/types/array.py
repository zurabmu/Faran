try:
    from beartype import beartype  # pyright: ignore[reportMissingImports]

    typechecker = beartype
except ImportError:
    typechecker = None

from typing import Protocol, runtime_checkable

from numpy.typing import NDArray
from jaxtyping import jaxtyped as jaxtyping_jaxtyped

import numpy as np

type Array = NDArray
type DataType = np.dtype


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
