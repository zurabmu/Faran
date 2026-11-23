from typing import Final
from dataclasses import dataclass, field
from pathlib import Path

from faran_visualizer.renderers import CanvasRenderer
from faran_visualizer.scene import Renderer
from faran_visualizer.theme import Theme

import anyio

type OutputPath = str | Path | anyio.Path
"""A path to save visualizations in."""

DEFAULT_THEME: Final = Theme.default()
DEFAULT_RENDERER: Final = CanvasRenderer()


@dataclass
class VisualizerConfig:
    """Global configuration for the visualizer."""

    output_directory: Path = Path.cwd() / "visualizations"
    theme: Theme = field(default_factory=Theme.default)
    renderer: Renderer = DEFAULT_RENDERER

    def configure(
        self,
        *,
        output_directory: OutputPath,
        theme: Theme = DEFAULT_THEME,
        renderer: Renderer = DEFAULT_RENDERER,
    ) -> None:
        """Configure the visualizer globally. Every setting is replaced, so a setting
        that is not passed returns to its default.

        Args:
            output_directory: The directory where visualizations will be saved.
            theme: The colors of the visualizations.
            renderer: The renderer used for generating the visualizations.
        """
        self.output_directory = Path(output_directory)
        self.theme = theme
        self.renderer = renderer


config: Final = VisualizerConfig()
configure: Final = config.configure
