import lazy_loader as lazy

# NOTE: These names are also subpackages. Importing a subpackage for the first time replaces the
# package attribute of the same name, so the subpackages are imported before the names are bound.
from . import noise as _noise  # noqa: F401
from .factory import noise as noise

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
