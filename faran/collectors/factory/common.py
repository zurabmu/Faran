from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.collectors.factory.basic import collectors as numpy_collectors

if TYPE_CHECKING:
    from faran.collectors.factory.accelerated import collectors as jax_collectors


class collectors:
    """Factory namespace for creating simulation data collectors."""

    numpy = numpy_collectors

    if TYPE_CHECKING:
        jax = jax_collectors
    else:
        jax = loaded_on_access(
            module="faran.collectors.factory.accelerated", name="collectors"
        )
