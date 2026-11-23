from typing import Sequence
from dataclasses import dataclass
from pathlib import Path

from faran_visualizer.scene import Animation


@dataclass(frozen=True)
class RerunRenderer:
    """Saves animations as Rerun visualizations (`.frn` files) and opens them in the
    Rerun viewer. It needs the `rerun` extra: `pip install faran-visualizer[rerun]`.

    Attributes:
        in_browser: Whether `view` opens the Rerun web viewer in the browser instead
            of the native viewer.
    """

    in_browser: bool = False

    @property
    def extension(self) -> str:
        return ".frn"

    def save(self, animation: Animation, *, to: Path) -> None:
        from faran_visualizer.renderers.rerun.visualization import save

        save(animation, name=to.stem, to=to)

    def view(self, visualizations: Sequence[Path]) -> None:
        """Opens the visualizations in the Rerun viewer and returns when it closes."""
        from faran_visualizer.renderers.rerun.viewer import view

        view(visualizations, in_browser=self.in_browser)

    def show(self, visualization: Path) -> None:
        from faran_visualizer.renderers.rerun.notebook import show

        show(visualization)
