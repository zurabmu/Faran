from typing import Sequence
from pathlib import Path

from faran_visualizer.renderers.rerun.notebook import show
from faran_visualizer.renderers.rerun.visualization import save
from faran_visualizer.renderers.rerun.viewer import view
from faran_visualizer.scene import Animation


class RerunRenderer:
    """Saves animations as Rerun visualizations and opens them in the Rerun viewer."""

    def save(self, animation: Animation, *, to: Path) -> None:
        save(animation, name=to.stem, to=to)

    def view(self, visualizations: Sequence[Path], *, in_browser: bool) -> None:
        view(visualizations, in_browser=in_browser)

    def show(self, visualization: Path) -> None:
        show(visualization)
