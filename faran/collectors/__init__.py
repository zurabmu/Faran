import lazy_loader as lazy

# NOTE: These names are also subpackages. Importing a subpackage for the first time replaces the
# package attribute of the same name, so the subpackages are imported before the names are bound.
from . import access as _access  # noqa: F401
from .access import access as access

__getattr__, __dir__, __all__ = lazy.attach_stub(__name__, __file__)
