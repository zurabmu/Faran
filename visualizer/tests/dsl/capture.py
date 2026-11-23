from typing import Sequence
from dataclasses import dataclass, field
from pathlib import Path

from faran_visualizer import (
    Scene,
    SimulationVisualizer,
    Theme,
)
from faran_visualizer.scene import Animation
from tests.dsl.visualization import Visualization


@dataclass
class CapturingRenderer:
    """A renderer that keeps every animation it is given in memory."""

    animations: list[Animation] = field(default_factory=list)

    @property
    def extension(self) -> str:
        return ".captured"

    def save(self, animation: Animation, *, to: Path) -> None:
        self.animations.append(animation)

    def view(self, visualizations: Sequence[Path]) -> None:
        raise NotImplementedError

    def show(self, visualization: Path) -> None:
        raise NotImplementedError


@dataclass(frozen=True)
class Visualize:
    """Runs a visualizer and returns what it hands to its renderer."""

    directory: Path

    async def scene(
        self, scene: Scene, *, theme: Theme = Theme.default()
    ) -> Visualization:
        renderer = CapturingRenderer()
        await SimulationVisualizer(
            output=self.directory, renderer=renderer, theme=theme
        )(scene, key="scene")
        return visualization_from(renderer)


def visualization_from(renderer: CapturingRenderer) -> Visualization:
    (animation,) = renderer.animations
    return Visualization(animation=animation)


class files:
    @staticmethod
    def in_directory(directory: Path) -> list[str]:
        return sorted(it.name for it in directory.iterdir())
