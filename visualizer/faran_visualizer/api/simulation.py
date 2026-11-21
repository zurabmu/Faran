from dataclasses import dataclass
from functools import partial
from pathlib import Path

from faran_visualizer.api.config import OutputPath, config
from faran_visualizer.api.renderer import default_renderer, visualization_path
from faran_visualizer.scene import Renderer, Scene, animation_from

import anyio


@dataclass(kw_only=True, frozen=True)
class SimulationVisualizer:
    output: Path
    renderer: Renderer

    @staticmethod
    def create(
        *,
        output: str = "simulation",
        output_directory: OutputPath | None = None,
    ) -> "SimulationVisualizer":
        """Creates a visualizer that saves visualizations in
        `<output_directory>/<output>`. Without `output_directory`, it uses the
        configured output directory."""
        directory = (
            Path(output_directory)
            if output_directory is not None
            else config.output_directory
        )
        return SimulationVisualizer(
            output=directory / output, renderer=default_renderer()
        )

    async def __call__(self, scene: Scene, *, key: str) -> None:
        """Saves the scene as a visualization at `<output>/<key>.frn`.

        Raises:
            InconsistentRenderingsError: If the steps of the scene render differently
                named renderings.
        """
        path = visualization_path(self.output, key=key)
        animation = animation_from(scene)

        await anyio.Path(self.output).mkdir(parents=True, exist_ok=True)
        await anyio.to_thread.run_sync(partial(self.renderer.save, animation, to=path))
        print(f"Saved: {path}")

    async def can_visualize(self, data: object) -> bool:
        return isinstance(data, Scene)
