import asyncio
from collections.abc import Callable, Coroutine, Iterator
from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import anyio.to_thread
from faran_visualizer import CanvasRenderer, configure

from .theme import dusk

type Scheduled = list[asyncio.Future[Any]]


class SnippetVisualizationError(Exception):
    """Raised when a documentation snippet does not save exactly one visualization."""


async def run_snippet(source: str) -> str:
    """Runs a documentation snippet as `__main__` and returns the JSON of the one
    visualization it saved. Leaves the visualizer configured for the canvas renderer.

    Raises:
        SnippetVisualizationError: If the snippet saved no visualization or more than one.
    """
    with TemporaryDirectory() as directory:
        output = Path(directory)
        save_canvas_visualizations_in(output)
        await run_as_main(source)
        return visualization_in(output)


def save_canvas_visualizations_in(output: Path) -> None:
    configure(output_directory=output, theme=dusk, renderer=CanvasRenderer())


async def run_as_main(source: str) -> None:
    with running_loop_only() as scheduled:
        exec(compile(source, "snippet.py", "exec"), {"__name__": "__main__"})
        await asyncio.gather(*scheduled)


@contextmanager
def running_loop_only() -> Iterator[Scheduled]:
    # Pyodide has no threads and cannot start a second event loop, so the snippet's
    # coroutines and the visualizer's thread work run on the running loop instead.
    scheduled: Scheduled = []
    with (
        replaced(asyncio, "run", scheduling_into(scheduled)),
        replaced(anyio.to_thread, "run_sync", run_in_calling_thread),
    ):
        yield scheduled


def scheduling_into(scheduled: Scheduled) -> Callable[..., None]:
    def schedule(main: Coroutine[Any, Any, Any], **_: object) -> None:
        scheduled.append(asyncio.ensure_future(main))

    return schedule


async def run_in_calling_thread(
    function: Callable[..., Any], *arguments: Any, **_: object
) -> Any:
    return function(*arguments)


@contextmanager
def replaced(owner: object, name: str, replacement: object) -> Iterator[None]:
    original = getattr(owner, name)
    setattr(owner, name, replacement)
    try:
        yield
    finally:
        setattr(owner, name, original)


def visualization_in(output: Path) -> str:
    saved = sorted(output.rglob("*.json"))
    if len(saved) != 1:
        raise SnippetVisualizationError(
            f"Expected the snippet to save one visualization, but it saved {len(saved)}: "
            f"{[path.name for path in saved]}."
        )
    return saved[0].read_text(encoding="utf-8")
