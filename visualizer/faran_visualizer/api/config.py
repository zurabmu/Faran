from typing import Final
from dataclasses import dataclass
from pathlib import Path

import anyio

type OutputPath = str | Path | anyio.Path
"""A path to save visualizations in."""


@dataclass
class VisualizerConfig:
    """Global configuration for the visualizer."""

    output_directory: Path = Path.cwd() / "visualizations"

    def configure(self, *, output_directory: OutputPath) -> None:
        """Configure the visualizer globally.

        Args:
            output_directory: The directory where visualizations will be saved.
        """
        self.output_directory = Path(output_directory)


config: Final = VisualizerConfig()
configure: Final = config.configure
