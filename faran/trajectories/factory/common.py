from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.trajectories.factory.basic import trajectory as numpy_trajectory

if TYPE_CHECKING:
    from faran.trajectories.factory.accelerated import trajectory as jax_trajectory


class trajectory:
    """Factory namespace for creating reference trajectories."""

    numpy = numpy_trajectory

    if TYPE_CHECKING:
        jax = jax_trajectory
    else:
        jax = loaded_on_access(
            module="faran.trajectories.factory.accelerated", name="trajectory"
        )
