from typing import Any, Callable, Concatenate
from dataclasses import dataclass, fields, is_dataclass
from functools import partial

from faran.types import Receiver, pytree, recording

from flax import nnx

import jax

_components: set[type] = set()


@dataclass(frozen=True, eq=False)
class SameObject:
    value: Any

    def __eq__(self, other: object) -> bool:
        return isinstance(other, SameObject) and other.value is self.value

    def __hash__(self) -> int:
        return id(self.value)


def compiled[OwnerT, **P, R](
    method: Callable[Concatenate[OwnerT, P], R],
) -> Callable[Concatenate[OwnerT, P], R]:
    """Compiles `method` as one JAX graph. Flax variables of the owner and of every dataclass
    it references keep their values from one call to the next, and values recorded during the
    call are delivered to their receivers after it.
    """
    receivers: dict[nnx.graph.GraphDef[OwnerT], list[Receiver[Any]]] = {}

    @partial(jax.jit, static_argnums=0)
    def run(
        graph: nnx.graph.GraphDef[OwnerT],
        state: nnx.State,
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> tuple[R, tuple[Any, ...], nnx.State]:
        owner = nnx.merge(graph, state)

        with recording() as records:
            result = method(owner, *args, **kwargs)

        receivers[graph] = records.receivers
        return result, tuple(records.values), nnx.state(owner, nnx.Variable)

    def call(owner: OwnerT, *args: P.args, **kwargs: P.kwargs) -> R:
        register(owner)
        graph, state = nnx.split(owner)
        result, values, variables = run(graph, state, *args, **kwargs)
        nnx.update(owner, variables)

        for receiver, value in zip(receivers[graph], values, strict=True):
            receiver.receive(value)

        return result

    return call


def register(component: Any) -> None:
    """Registers `component`, and every component it references, as a Flax graph node. A
    component must be registered before it is passed to a function compiled with `nnx.jit`.
    """
    if isinstance(component, (list, tuple)):
        for item in component:
            register(item)
    elif is_component(component):
        register_type(type(component))

        for item in vars(component).values():
            register(item)


def is_component(value: Any) -> bool:
    return (
        is_dataclass(value)
        and not isinstance(value, type)
        and (type(value) in _components or not nnx.graph.is_node(value))
    )


def register_type(component: type) -> None:
    if component in _components:
        return

    nnx.graph.register_graph_node_type(
        component,
        flatten=flatten,
        set_key=lambda node, key, value: object.__setattr__(node, str(key), value),
        pop_key=lambda node, key: vars(node).pop(key),
        create_empty=lambda component: object.__new__(component),
        clear=lambda node: vars(node).clear(),
        init=initialize,
    )
    _components.add(component)


def flatten(node: Any) -> tuple[list[tuple[str, Any]], type]:
    static = {field.name for field in fields(node) if pytree.is_static(field)}
    return [
        (name, nnx.graph.StaticElem(SameObject(value)) if name in static else value)
        for name, value in sorted(vars(node).items())
    ], type(node)


def initialize(node: Any, attributes: Any) -> None:
    for name, value in attributes:
        object.__setattr__(
            node, name, value.value if isinstance(value, SameObject) else value
        )
