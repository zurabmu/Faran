from typing import Protocol

from faran import ControlInputSequence, ReferencePoints, Trajectory, trajectory, types
from faran_visualizer import Array, JaxArray

from numpy.typing import ArrayLike
from jaxtyping import Float

import numpy as np
import jax.numpy as jnp

type NumPyStates = types.numpy.augmented.StateSequence[
    types.numpy.bicycle.StateSequence, types.numpy.simple.StateSequence
]
type JaxStates = types.jax.augmented.StateSequence[
    types.jax.bicycle.StateSequence, types.jax.simple.StateSequence
]
type States = NumPyStates | JaxStates
type Reference = Trajectory[types.numpy.PathParameters, ReferencePoints]


class Backend(Protocol):
    """Builds Faran objects with the arrays of one numerical backend."""

    def array(self, values: ArrayLike) -> Float[Array, "..."] | Float[JaxArray, "..."]:
        """Returns the values as an array of this backend."""
        ...

    def states(
        self, *, physical: Float[Array, "T 4"], virtual: Float[Array, "T 1"]
    ) -> States:
        """Returns bicycle states augmented with a path parameter."""
        ...

    def reference(self, *, path_length: float) -> Reference:
        """Returns a straight reference along the x axis."""
        ...

    def no_inputs(self) -> ControlInputSequence:
        """Returns a control input sequence of zeros."""
        ...


class NumPyBackend:
    def array(self, values: ArrayLike) -> Float[Array, "..."]:
        return np.asarray(values, dtype=float)

    def states(
        self, *, physical: Float[Array, "T 4"], virtual: Float[Array, "T 1"]
    ) -> NumPyStates:
        return types.numpy.augmented.state_sequence.of(
            physical=types.numpy.bicycle.state_sequence(
                batch=types.numpy.bicycle.state_batch.wrap(physical[..., None]),
                rollout=0,
            ),
            virtual=types.numpy.simple.state_sequence(virtual),
        )

    def reference(self, *, path_length: float) -> Reference:
        return trajectory.numpy.line(start=(0.0, 0.0), end=(path_length, 0.0))

    def no_inputs(self) -> ControlInputSequence:
        return types.numpy.bicycle.control_input_sequence(np.zeros((1, 2)))


class JaxBackend:
    def array(self, values: ArrayLike) -> Float[JaxArray, "..."]:
        return jnp.asarray(values, dtype=float)

    def states(
        self, *, physical: Float[Array, "T 4"], virtual: Float[Array, "T 1"]
    ) -> JaxStates:
        return types.jax.augmented.state_sequence.of(
            physical=types.jax.bicycle.state_sequence(
                batch=types.jax.bicycle.state_batch.wrap(
                    self.array(physical[..., None])
                ),
                rollout=0,
            ),
            virtual=types.jax.simple.state_sequence(self.array(virtual)),
        )

    def reference(self, *, path_length: float) -> Reference:
        return trajectory.jax.line(start=(0.0, 0.0), end=(path_length, 0.0))

    def no_inputs(self) -> ControlInputSequence:
        return types.jax.bicycle.control_input_sequence(self.array(np.zeros((1, 2))))
