from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.samplers.factory.basic import sampler as numpy_sampler

if TYPE_CHECKING:
    from faran.samplers.factory.accelerated import sampler as jax_sampler


class sampler:
    numpy = numpy_sampler

    if TYPE_CHECKING:
        jax = jax_sampler
    else:
        jax = loaded_on_access(
            module="faran.samplers.factory.accelerated", name="sampler"
        )
