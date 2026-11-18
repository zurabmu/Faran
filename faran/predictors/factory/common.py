from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.predictors.factory.basic import predictor as numpy_predictor

if TYPE_CHECKING:
    from faran.predictors.factory.accelerated import predictor as jax_predictor


class predictor:
    """Factory namespace for creating obstacle motion predictors."""

    numpy = numpy_predictor

    if TYPE_CHECKING:
        jax = jax_predictor
    else:
        jax = loaded_on_access(
            module="faran.predictors.factory.accelerated", name="predictor"
        )
