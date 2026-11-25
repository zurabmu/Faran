from typing import Any

from griffe import Class, Extension, Function, Module


class PrivateParameters(Extension):
    """Removes parameters whose names start with an underscore from constructor signatures.

    Must run after griffe's `dataclasses` extension, which creates the constructors of
    dataclasses. A class whose constructor takes only private parameters gets no signature.
    """

    # griffe's Extension.on_package declares **kwargs: Any, which an override must accept.
    def on_package(self, *, pkg: Module, **kwargs: Any) -> None:
        remove_private_parameters(pkg)


def remove_private_parameters(parent: Module | Class) -> None:
    for member in parent.members.values():
        if member.is_alias:
            continue

        if isinstance(member, Class):
            remove_private_constructor_parameters(member)

        if isinstance(member, Module | Class):
            remove_private_parameters(member)


def remove_private_constructor_parameters(cls: Class) -> None:
    constructor = cls.members.get("__init__")

    if not isinstance(constructor, Function):
        return

    private = [
        parameter.name
        for parameter in constructor.parameters
        if is_private(parameter.name)
    ]

    if not private:
        return

    for name in private:
        del constructor.parameters[name]

    if not has_public_parameters(constructor):
        del cls.members["__init__"]


def has_public_parameters(constructor: Function) -> bool:
    return any(parameter.name != "self" for parameter in constructor.parameters)


def is_private(name: str) -> bool:
    return name.startswith("_") and not name.startswith("__")
