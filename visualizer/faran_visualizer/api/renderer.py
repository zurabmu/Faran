from typing import Final, Sequence
from pathlib import Path

from faran_visualizer.renderers import CanvasRenderer, RerunRenderer
from faran_visualizer.scene import Renderer

RENDERERS: Final[tuple[Renderer, ...]] = (RerunRenderer(), CanvasRenderer())


class UnknownVisualizationError(ValueError):
    """Raised when a file's extension belongs to no renderer."""


def renderer_for(
    visualization: Path, *, renderers: Sequence[Renderer] = RENDERERS
) -> Renderer:
    """Returns the first of `renderers` that saves visualizations with the file's
    extension.

    Raises:
        UnknownVisualizationError: If none of `renderers` saves files with that
            extension.
    """
    for renderer in renderers:
        if visualization.suffix == renderer.extension:
            return renderer
    raise UnknownVisualizationError(
        f"No renderer opens {visualization}. Expected one of the extensions "
        f"{', '.join(renderer.extension for renderer in renderers)}, "
        f"but the file has '{visualization.suffix}'."
    )


def visualization_path(directory: Path, *, key: str, renderer: Renderer) -> Path:
    """Returns the path of the visualization that `renderer` saves under `key`."""
    return directory / f"{key}{renderer.extension}"
