from typing import Callable, Sequence
from dataclasses import dataclass

from faran_visualizer.array import Array
from faran_visualizer.data import Plots
from faran_visualizer.scene.colors import color as color_from
from faran_visualizer.scene.animation import (
    DotStyle,
    Dots,
    Rendering,
    LinePattern,
    Lines,
    LineStyle,
    Points,
)

from jaxtyping import Float


class render:
    @staticmethod
    def lines(
        *,
        name: str,
        label: str,
        strips: Sequence[Points],
        color: str,
        width: float = 2.0,
        pattern: LinePattern = "solid",
    ) -> Rendering:
        """Renders polylines through the points of each strip. `width` is in screen
        points. `label` is the text of the legend entry, which renderings with the same
        label share.

        Raises:
            InvalidColorError: If the color is not supported.
        """
        return Lines(
            name=name,
            label=label,
            strips=strips,
            style=LineStyle(color=color_from(color), width=width, pattern=pattern),
        )

    @staticmethod
    def dots(
        *, name: str, label: str, positions: Points, color: str, size: float = 4.0
    ) -> Rendering:
        """Renders a dot at each position. `size` is the dot diameter in screen points.
        `label` is the text of the legend entry, which renderings with the same label
        share.

        Raises:
            InvalidColorError: If the color is not supported.
        """
        return Dots(
            name=name,
            label=label,
            positions=positions,
            style=DotStyle(color=color_from(color), size=size),
        )


@dataclass(kw_only=True, frozen=True)
class Info:
    """A row of the info table, with one value per step."""

    label: str
    values: Float[Array, " T"]
    unit: str | None = None


def no_renderings(step: int) -> Sequence[Rendering]:
    return []


@dataclass(kw_only=True, frozen=True)
class Scene:
    """What to show for a simulation: renderings in the x-y plane, plots over time,
    and an info table.

    Attributes:
        time_step: The time between two steps, in seconds.
        step_count: The number of steps.
        background: Renderings shown at every step, below the renderings of the step.
        at_step: Returns the renderings of a step. Every step must return renderings
            with the same names, in the same order.
        plots: The plots shown next to the scene.
        info: The rows of the info table.
    """

    time_step: float
    step_count: int
    background: Sequence[Rendering] = ()
    at_step: Callable[[int], Sequence[Rendering]] = no_renderings
    plots: Plots = ()
    info: Sequence[Info] = ()
