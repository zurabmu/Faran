from typing import TYPE_CHECKING
from importlib import import_module

from numpy.typing import NDArray

type Array = NDArray

if TYPE_CHECKING:
    import jax

    type JaxArray = jax.Array
else:
    # NOTE: JAX is optional, so it is imported only when the alias is evaluated.
    type JaxArray = import_module("jax").Array
