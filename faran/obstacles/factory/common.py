from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.obstacles.factory.basic import obstacles as numpy_obstacles

if TYPE_CHECKING:
    from faran.obstacles.factory.accelerated import obstacles as jax_obstacles


class obstacles:
    numpy = numpy_obstacles

    if TYPE_CHECKING:
        jax = jax_obstacles
    else:
        jax = loaded_on_access(
            module="faran.obstacles.factory.accelerated", name="obstacles"
        )
