from typing import Sequence
from pathlib import Path

from faran_visualizer.api.renderer import default_renderer


def show(visualization: str | Path) -> None:
    """Shows a `.frn` visualization in the output of the current Jupyter notebook cell."""
    default_renderer().show(Path(visualization))


def view(visualizations: Sequence[str | Path], *, in_browser: bool = False) -> None:
    """Opens `.frn` visualizations in a viewer and returns when the viewer closes."""
    default_renderer().view([Path(it) for it in visualizations], in_browser=in_browser)
