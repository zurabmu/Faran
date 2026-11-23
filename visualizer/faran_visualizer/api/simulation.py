from dataclasses import dataclass
from functools import partial
from pathlib import Path

from faran_visualizer.api.config import OutputPath, config
from faran_visualizer.api.renderer import visualization_path
from faran_visualizer.scene import Renderer, Scene, animation_from
from faran_visualizer.theme import Theme

import anyio


@dataclass(kw_only=True, frozen=True)
class SimulationVisualizer:
    output: Path
    renderer: Renderer
    theme: Theme

    @staticmethod
    def create(
        *,
        output: str = "simulation",
        output_directory: OutputPath | None = None,
        theme: Theme | None = None,
        renderer: Renderer | None = None,
    ) -> "SimulationVisualizer":
        """Creates a visualizer that saves visualizations in
        `<output_directory>/<output>`. Omitted configuration values
        are taken from the global configuration."""
        directory = (
            Path(output_directory)
            if output_directory is not None
            else config.output_directory
        )
        return SimulationVisualizer(
            output=directory / output,
            renderer=renderer if renderer is not None else config.renderer,
            theme=theme if theme is not None else config.theme,
        )

    async def __call__(self, scene: Scene, *, key: str) -> None:
        """Saves the scene as a visualization at `<output>/<key>` with the extension
        of the renderer.

        Raises:
            InconsistentRenderingsError: If the steps of the scene render differently
                named renderings.
        """
        path = visualization_path(self.output, key=key, renderer=self.renderer)
        animation = animation_from(scene, theme=self.theme)

        await anyio.Path(self.output).mkdir(parents=True, exist_ok=True)
        await anyio.to_thread.run_sync(partial(self.renderer.save, animation, to=path))
        print(f"Saved: {path}")

    async def can_visualize(self, data: object) -> bool:
        return isinstance(data, Scene)
