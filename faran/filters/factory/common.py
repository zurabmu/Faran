from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.filters.factory.basic import noise as numpy_noise

if TYPE_CHECKING:
    from faran.filters.factory.accelerated import noise as jax_noise


class noise:
    """Factory namespace for noise model providers."""

    numpy = numpy_noise

    if TYPE_CHECKING:
        jax = jax_noise
    else:
        jax = loaded_on_access(module="faran.filters.factory.accelerated", name="noise")
