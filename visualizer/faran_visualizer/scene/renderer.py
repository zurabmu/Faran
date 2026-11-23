from typing import Protocol, Sequence
from pathlib import Path

from faran_visualizer.scene.animation import Animation


class Renderer(Protocol):
    @property
    def extension(self) -> str:
        """The file extension of the visualizations it saves, with the leading dot."""
        ...

    def save(self, animation: Animation, *, to: Path) -> None:
        """Saves the animation as a visualization file that `view` and `show` can open."""
        ...

    def view(self, visualizations: Sequence[Path]) -> None:
        """Opens the visualizations in a viewer."""
        ...

    def show(self, visualization: Path) -> None:
        """Shows the visualization in the output of the current Jupyter notebook cell."""
        ...
