from typing import Protocol, Any, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field


class Receiver[T](Protocol):
    """Receives values recorded for it."""

    def receive(self, value: T, /) -> None:
        """Takes one recorded value."""
        ...


class Recorder(Protocol):
    def record[T](self, receiver: Receiver[T], value: T) -> None:
        """Records `value` for the specified `receiver`."""
        ...


class DirectDelivery:
    """A simple recorder that delivers values directly to receivers."""

    def record[T](self, receiver: Receiver[T], value: T) -> None:
        receiver.receive(value)


@dataclass
class Records:
    """Values recorded while a `recording` block runs, in the order they were recorded."""

    receivers: list[Receiver[Any]] = field(default_factory=list)
    values: list[Any] = field(default_factory=list)

    def record[T](self, receiver: Receiver[T], value: T) -> None:
        self.receivers.append(receiver)
        self.values.append(value)


_recorder: ContextVar[Recorder] = ContextVar("recorder", default=DirectDelivery())


def record[T](receiver: Receiver[T], value: T) -> None:
    """Delivers `value` to `receiver`. Inside a `recording` block, the value is stored in the
    block's records instead, and the code that runs the block delivers it.
    """
    _recorder.get().record(receiver, value)


@contextmanager
def recording() -> Iterator[Records]:
    """Stores the values recorded inside the block in the returned records."""
    token = _recorder.set(records := Records())
    try:
        yield records
    finally:
        _recorder.reset(token)
