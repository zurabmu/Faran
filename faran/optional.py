from importlib import import_module
from typing import Any


class loaded_on_access:
    """Class attribute that imports `name` from `module` when it is first read.

    Raises `ModuleNotFoundError` on access when `module` needs a package that is not installed.
    """

    def __init__(self, *, module: str, name: str) -> None:
        self.module = module
        self.name = name

    def __get__(self, instance: object, owner: type) -> Any:
        return getattr(import_module(self.module), self.name)
