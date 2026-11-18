from needy import needs
from tests.dsl import probe

from . import basic as basic

with needs.modules(probe.jax):
    from . import accelerated as accelerated
