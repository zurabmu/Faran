from typing import Sequence
from itertools import groupby
from pathlib import Path

from faran_visualizer.api.renderer import RENDERERS, renderer_for
from faran_visualizer.scene import Renderer


def show(visualization: str | Path) -> None:
    """Shows a visualization in the output of the current Jupyter notebook cell, with
    the renderer that saves files with its extension.

    Raises:
        UnknownVisualizationError: If no renderer saves files with its extension.
    """
    path = Path(visualization)
    renderer_for(path).show(path)


def view(
    visualizations: Sequence[str | Path], *, renderers: Sequence[Renderer] = RENDERERS
) -> None:
    """Opens visualizations in the viewer of the first of `renderers` that saves files
    with their extension, one renderer after another.

    Raises:
        UnknownVisualizationError: If none of `renderers` saves files with one of the
            extensions.
    """
    paths = [Path(it) for it in visualizations]
    for renderer, group in groupby(
        paths, key=lambda path: renderer_for(path, renderers=renderers)
    ):
        renderer.view(list(group))
