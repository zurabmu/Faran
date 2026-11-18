from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.costs.factory.basic import (
    costs as numpy_costs,
    distance as numpy_distance,
    boundary as numpy_boundary,
)

if TYPE_CHECKING:
    from faran.costs.factory.accelerated import (
        costs as jax_costs,
        distance as jax_distance,
        boundary as jax_boundary,
    )


class costs:
    numpy = numpy_costs

    if TYPE_CHECKING:
        jax = jax_costs
    else:
        jax = loaded_on_access(module="faran.costs.factory.accelerated", name="costs")


class distance:
    numpy = numpy_distance

    if TYPE_CHECKING:
        jax = jax_distance
    else:
        jax = loaded_on_access(
            module="faran.costs.factory.accelerated", name="distance"
        )


class boundary:
    numpy = numpy_boundary

    if TYPE_CHECKING:
        jax = jax_boundary
    else:
        jax = loaded_on_access(
            module="faran.costs.factory.accelerated", name="boundary"
        )
