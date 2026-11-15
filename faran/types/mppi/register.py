from faran.types.pytree import pytree
from faran.types.mppi.common import Control, DebugData


def register_shared_types_as_pytrees() -> None:
    pytree(Control)
    pytree(DebugData)
