import lazy_loader as lazy

# NOTE: These names are also subpackages. Importing a subpackage for the first time replaces the
# package attribute of the same name, so the subpackages are imported before the names are bound.
from . import distance as _distance, boundary as _boundary, risk as _risk  # noqa: F401
from .factory import distance as distance, boundary as boundary
from .risk import risk as risk

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
