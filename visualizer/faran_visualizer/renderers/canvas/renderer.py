from typing import Sequence
from pathlib import Path

from faran_visualizer.renderers.canvas.encoding import animation_json, frame_json
from faran_visualizer.renderers.canvas.notebook import show
from faran_visualizer.renderers.canvas.viewer import view
from faran_visualizer.scene import Animation, Frame, Rendering


class CanvasRenderer:
    """Saves animations as JSON visualizations (`.json` files) that a canvas engine in
    the browser draws. It needs no packages beyond the visualizer's own, so it also
    works in Pyodide."""

    @property
    def extension(self) -> str:
        return ".json"

    def save(self, animation: Animation, *, to: Path) -> None:
        _ = to.write_text(animation_json(animation), encoding="utf-8")

    def view(self, visualizations: Sequence[Path]) -> None:
        """Opens each visualization in the default browser and returns once they are
        open."""
        view(visualizations)

    def show(self, visualization: Path) -> None:
        show(visualization)

    @staticmethod
    def frame_json(*, renderings: Sequence[Rendering]) -> str:
        """Returns one frame of renderings in the JSON form that the canvas engine
        draws, for drawing frames as they are computed instead of saving an animation."""
        return frame_json(Frame(renderings=renderings, info=[]))
