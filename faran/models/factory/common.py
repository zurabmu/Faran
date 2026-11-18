from typing import TYPE_CHECKING

from faran.optional import loaded_on_access
from faran.models.factory.basic import model as numpy_model

if TYPE_CHECKING:
    from faran.models.factory.accelerated import model as jax_model


class model:
    numpy = numpy_model

    if TYPE_CHECKING:
        jax = jax_model
    else:
        jax = loaded_on_access(module="faran.models.factory.accelerated", name="model")
