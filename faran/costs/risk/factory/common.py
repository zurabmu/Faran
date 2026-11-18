from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.costs.risk.factory.basic import risk as numpy_risk

if TYPE_CHECKING:
    from faran.costs.risk.factory.accelerated import risk as jax_risk


class risk:
    """Factory namespace for creating risk metrics with different risk measures."""

    numpy = numpy_risk

    if TYPE_CHECKING:
        jax = jax_risk
    else:
        jax = loaded_on_access(
            module="faran.costs.risk.factory.accelerated", name="risk"
        )
