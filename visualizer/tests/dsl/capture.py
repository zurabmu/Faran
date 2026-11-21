from typing import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from faran_visualizer import (
    Scene,
    SimulationVisualizer,
)
from faran_visualizer.scene import Animation
from tests.dsl.visualization import Visualization


@dataclass
class CapturingRenderer:
    """A renderer that keeps every animation it is given in memory."""

    animations: list[Animation] = field(default_factory=list)

    def save(self, animation: Animation, *, to: Path) -> None:
        self.animations.append(animation)

    def view(self, visualizations: Sequence[Path], *, in_browser: bool) -> None:
        raise NotImplementedError

    def show(self, visualization: Path) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class Visualize:
    """Runs a visualizer and returns what it hands to its renderer."""

    directory: Path

    async def scene(self, scene: Scene) -> Visualization:
        renderer = CapturingRenderer()
        await SimulationVisualizer(output=self.directory, renderer=renderer)(
            scene, key="scene"
        )
        return visualization_from(renderer)


def visualization_from(renderer: CapturingRenderer) -> Visualization:
    (animation,) = renderer.animations
    return Visualization(animation=animation)


class files:
    @staticmethod
    def in_directory(directory: Path) -> list[str]:
        return sorted(it.name for it in directory.iterdir())
