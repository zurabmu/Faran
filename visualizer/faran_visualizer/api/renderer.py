from typing import Final
from pathlib import Path

from faran_visualizer.renderers import RerunRenderer
from faran_visualizer.scene import Renderer

VISUALIZATION_EXTENSION: Final = ".frn"


def default_renderer() -> Renderer:
    return RerunRenderer()


def visualization_path(directory: Path, *, key: str) -> Path:
    """Returns the path of the visualization file saved under `key`."""
    return directory / f"{key}{VISUALIZATION_EXTENSION}"
