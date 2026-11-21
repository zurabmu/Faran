from faran_visualizer.array import Array

from typing import Literal, NamedTuple, Sequence
from dataclasses import dataclass

from jaxtyping import Float

type Points = Float[Array, "N 2"]
"""An (N, 2) array of x-y points."""

type LinePattern = Literal["solid", "dashed", "dotted"]
type ChartScale = Literal["linear", "log"]


class Color(NamedTuple):
    red: int
    green: int
    blue: int
    alpha: int


@dataclass(kw_only=True, frozen=True)
class LineStyle:
    """`width` is in screen points."""

    color: Color
    width: float
    pattern: LinePattern = "solid"


@dataclass(kw_only=True, frozen=True)
class DotStyle:
    """`size` is the dot diameter in screen points."""

    color: Color
    size: float


@dataclass(kw_only=True, frozen=True)
class Lines:
    name: str
    strips: Sequence[Points]
    style: LineStyle


@dataclass(kw_only=True, frozen=True)
class Dots:
    name: str
    positions: Points
    style: DotStyle


type Rendering = Lines | Dots
"""Something rendered in the x-y plane. Its name is the name it has in the viewer."""


class Row(NamedTuple):
    """A row of the info table at one step."""

    label: str
    value: float
    unit: str | None


@dataclass(kw_only=True, frozen=True)
class Frame:
    """What is shown at one step. Later renderings are rendered on top."""

    renderings: Sequence[Rendering]
    info: Sequence[Row]


@dataclass(kw_only=True, frozen=True)
class PlotLine:
    """One line of a chart, with one value per step."""

    name: str
    values: Float[Array, " N"]
    style: LineStyle


@dataclass(kw_only=True, frozen=True)
class Chart:
    id: str
    title: str
    y_label: str
    scale: ChartScale
    lines: Sequence[PlotLine]


@dataclass(kw_only=True, frozen=True)
class Animation:
    """A scene with every step rendered and every style resolved, in the form a
    renderer saves. Background renderings are rendered below the renderings of every
    frame."""

    time_step: float
    background: Sequence[Rendering]
    frames: Sequence[Frame]
    charts: Sequence[Chart]
