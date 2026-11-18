from dataclasses import Field, dataclass, field
from typing import Any, Callable, Final

from jax.tree_util import register_dataclass
from jax.core import Tracer
from flax import nnx

import jax
import jax.numpy as jnp

_STATIC: Final = {"static": True}


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

    @staticmethod
    def variable[T](value: T) -> "pytree.Variable[T]":
        """Creates a value that a compiled planner step can replace. The step's last value is kept
        for the next step.
        """
        return pytree.Variable(nnx.Variable(value))

    @dataclass(frozen=True)
    class Variable[T]:
        """A value that a compiled planner step can replace. Created with `pytree.variable`."""

        _cell: nnx.Variable[T]

        def get(self) -> T:
            value = self._cell.get_value()

            if not is_traced(value) and is_inside_trace():
                raise UntracedStateError(
                    "The state of a component was read inside a compiled function that does not "
                    "receive the state as an input, so the compiled function would not see the "
                    "latest value of the state. Register the component with `faran.jax.register` "
                    "and pass it as an argument to a function compiled with `nnx.jit`."
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
