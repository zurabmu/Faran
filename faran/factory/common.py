from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.factory.basic import (
    mppi as numpy_mppi,
    update as numpy_update,
    padding as numpy_padding,
    filters as numpy_filters,
)

if TYPE_CHECKING:
    from faran.factory.accelerated import (
        mppi as jax_mppi,
        update as jax_update,
        padding as jax_padding,
        filters as jax_filters,
    )


class mppi:
    """Factory namespace for creating MPPI planners."""

    numpy = numpy_mppi

    if TYPE_CHECKING:
        jax = jax_mppi
    else:
        jax = loaded_on_access(module="faran.factory.accelerated", name="mppi")


class update:
    """Factory namespace for MPPI control sequence update strategies."""

    numpy = numpy_update

    if TYPE_CHECKING:
        jax = jax_update
    else:
        jax = loaded_on_access(module="faran.factory.accelerated", name="update")


class padding:
    """Factory namespace for MPPI control sequence padding strategies."""

    numpy = numpy_padding

    if TYPE_CHECKING:
        jax = jax_padding
    else:
        jax = loaded_on_access(module="faran.factory.accelerated", name="padding")


class filters:
    """Factory namespace for MPPI control sequence filtering strategies."""

    numpy = numpy_filters

    if TYPE_CHECKING:
        jax = jax_filters
    else:
        jax = loaded_on_access(module="faran.factory.accelerated", name="filters")
