from faran_visualizer.array import Array

from typing import Literal, Sequence
from dataclasses import dataclass

from jaxtyping import Float

import numpy as np


class Types:
    type Vehicle = Literal["triangle", "car", "circle"]
    type ObstacleShape = Literal["rectangle", "circle"]
    type Scale = Literal["linear", "log"]
    type Marking = Literal["solid", "dashed", "none"]


@dataclass(kw_only=True, frozen=True, eq=False)
class Plot:
    """A time series plot shown next to the scene, with its values over the steps of
    a simulation.

    Keep the plot object to refer to the plot later. Two plots are the same plot only
    if they are the same object.

    Attributes:
        name: The title of the plot.
        lines: The lines of the plot.
        bands: Ranges between a lower and an upper line.
        bounds: Limits shown as guide lines.
        unit: The unit of the plotted values, shown on the y axis.
        scale: Whether the y axis is linear or logarithmic.
    """

    name: str
    lines: "Sequence[Plot.Line]" = ()
    bands: "Sequence[Plot.Band]" = ()
    bounds: "Sequence[Plot.Bound]" = ()
    unit: str | None = None
    scale: Types.Scale = "linear"

    @staticmethod
    def line(
        *,
        name: str,
        values: Float[Array, " T"],
        unit: str | None = None,
        scale: Types.Scale = "linear",
        color: str | None = None,
        bounds: "Sequence[Plot.Bound]" = (),
    ) -> "Plot":
        """Creates a plot with one line, labeled after the plot."""
        return Plot(
            name=name,
            lines=[Plot.Line(label=name, values=values, color=color)],
            bounds=bounds,
            unit=unit,
            scale=scale,
        )

    @property
    def step_counts(self) -> list[int]:
        """The number of steps of every array of the plot. Constant bounds have no
        steps."""
        return [
            np.shape(values)[0]
            for values in (
                *(line.values for line in self.lines),
                *(band.lower for band in self.bands),
                *(band.upper for band in self.bands),
                *(bound.values for bound in self.bounds),
            )
            if np.ndim(values) > 0
        ]

    @dataclass(kw_only=True, frozen=True, eq=False)
    class Chart:
        """Plots rendered together in one chart, with one y axis. The unit and scale of
        the chart apply to all of its plots.

        Attributes:
            name: The title of the chart.
            plots: The plots rendered in the chart.
            unit: The unit of the plotted values, shown on the y axis.
            scale: Whether the y axis is linear or logarithmic.
        """

        name: str
        plots: "Sequence[Plot]"
        unit: str | None = None
        scale: Types.Scale = "linear"

    @dataclass(frozen=True)
    class Line:
        """A line with one value per step."""

        label: str
        values: Float[Array, " T"]
        color: str | None = None

    @dataclass(frozen=True)
    class Band:
        """A range between a lower and an upper line, with one value per step.

        Attributes:
            label: The name of the band.
            lower: The value of the lower line at each step.
            upper: The value of the upper line at each step.
            lower_label: The name of the lower line in the legend, or
                `"<label> (lower)"` if not given.
            upper_label: The name of the upper line in the legend, or
                `"<label> (upper)"` if not given.
            color: The color of both lines.
        """

        label: str
        lower: Float[Array, " T"]
        upper: Float[Array, " T"]
        lower_label: str | None = None
        upper_label: str | None = None
        color: str | None = None

        @property
        def lower_name(self) -> str:
            """The name of the lower line in the legend."""
            return (
                self.lower_label
                if self.lower_label is not None
                else f"{self.label} (lower)"
            )

        @property
        def upper_name(self) -> str:
            """The name of the upper line in the legend."""
            return (
                self.upper_label
                if self.upper_label is not None
                else f"{self.label} (upper)"
            )

        def __post_init__(self) -> None:
            assert len(self.lower) == len(self.upper), (
                f"Band '{self.label}' has {len(self.lower)} lower and "
                f"{len(self.upper)} upper values."
            )

    @dataclass(frozen=True)
    class Bound:
        """A limit shown as a guide line, constant or with one value per step."""

        label: str
        values: Float[Array, " T"] | float


type Plots = Sequence[Plot | Plot.Chart]
"""Plots shown next to the scene: single plots, and charts of several plots."""


def plots_in(entry: Plot | Plot.Chart) -> Sequence[Plot]:
    """Returns the plots of a chart, or the plot itself."""
    match entry:
        case Plot.Chart():
            return entry.plots
        case Plot():
            return [entry]


class Road:
    @dataclass(kw_only=True, frozen=True)
    class Lane:
        x: Float[Array, " T"]
        y: Float[Array, " T"]
        boundaries: tuple[float, float]
        markings: tuple[Types.Marking, Types.Marking] = ("none", "none")

        def __post_init__(self) -> None:
            assert len(self.x) == len(self.y), (
                f"Lane x and y must have the same length. "
                f"Got {len(self.x)} (x) and {len(self.y)} (y)."
            )
            assert (
                width := (left := self.boundaries[0]) + (right := self.boundaries[1])
            ) > 0, (
                f"The width of the lane must be positive. Got {left} (left) + {right} (right) <= {width} (width)."
            )

    @dataclass(kw_only=True, frozen=True)
    class Network:
        lanes: Sequence["Road.Lane"]

        @staticmethod
        def empty() -> "Road.Network":
            return Road.Network(lanes=[])
