from typing import Protocol, Sequence
from pathlib import Path

from faran_visualizer.scene.animation import Animation


class Renderer(Protocol):
    def save(self, animation: Animation, *, to: Path) -> None:
        """Saves the animation as a visualization file that `view` and `show` can open."""
        ...

    def view(self, visualizations: Sequence[Path], *, in_browser: bool) -> None:
        """Opens the visualizations in a viewer and returns when the viewer closes."""
        ...

    def show(self, visualization: Path) -> None:
        """Shows the visualization in the output of the current Jupyter notebook cell."""
        ...
