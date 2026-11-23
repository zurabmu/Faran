from typing import Final, Sequence, cast
import math

import msgspec
import numpy as np
from jaxtyping import Float

from faran_visualizer.array import Array

from faran_visualizer.scene import (
    Animation,
    Chart,
    ChartScale,
    Color,
    Dots,
    DotStyle,
    Frame,
    LegendEntry,
    LinePattern,
    Lines,
    LineStyle,
    Points,
    Rendering,
    Row,
)

DECIMALS: Final = 3

type ColorJson = tuple[int, int, int, int]
type PointsJson = list[list[float]]


class LineStyleJson(msgspec.Struct):
    color: ColorJson
    width: float
    pattern: LinePattern


class DotStyleJson(msgspec.Struct):
    color: ColorJson
    size: float


class LinesJson(msgspec.Struct, tag_field="kind", tag="lines"):
    name: str
    strips: list[PointsJson]
    style: LineStyleJson


class DotsJson(msgspec.Struct, tag_field="kind", tag="dots"):
    name: str
    positions: PointsJson
    style: DotStyleJson


class RowJson(msgspec.Struct):
    label: str
    value: float
    unit: str


class FrameJson(msgspec.Struct):
    renderings: list[LinesJson | DotsJson]
    info: list[RowJson]


class LineMarkJson(msgspec.Struct, tag_field="kind", tag="line"):
    color: ColorJson
    width: float
    pattern: LinePattern


class DotMarkJson(msgspec.Struct, tag_field="kind", tag="dot"):
    color: ColorJson
    size: float


class LegendEntryJson(msgspec.Struct):
    label: str
    marks: list[LineMarkJson | DotMarkJson]


class ChartLineJson(msgspec.Struct):
    name: str
    values: list[float]
    style: LineStyleJson


class ChartJson(msgspec.Struct, rename="camel"):
    id: str
    title: str
    y_label: str
    scale: ChartScale
    lines: list[ChartLineJson]


class AnimationJson(msgspec.Struct, rename="camel"):
    time_step: float
    background_color: ColorJson
    background: list[LinesJson | DotsJson]
    frames: list[FrameJson]
    charts: list[ChartJson]
    legend: list[LegendEntryJson]


def animation_json(animation: Animation) -> str:
    """Returns the animation in the JSON form that the canvas engine draws."""
    return encoded(
        AnimationJson(
            time_step=animation.time_step,
            background_color=color_of(animation.background_color),
            background=renderings_of(animation.background),
            frames=[frame_of(frame) for frame in animation.frames],
            charts=[chart_of(chart) for chart in animation.charts],
            legend=[entry_of(entry) for entry in animation.legend],
        )
    )


def frame_json(frame: Frame) -> str:
    """Returns one frame in the JSON form that the canvas engine draws."""
    return encoded(frame_of(frame))


def encoded(value: msgspec.Struct) -> str:
    return msgspec.json.encode(value).decode()


def frame_of(frame: Frame) -> FrameJson:
    return FrameJson(
        renderings=renderings_of(frame.renderings),
        info=[row_of(row) for row in frame.info],
    )


def renderings_of(renderings: Sequence[Rendering]) -> list[LinesJson | DotsJson]:
    return [rendering_of(rendering) for rendering in renderings]


def rendering_of(rendering: Rendering) -> LinesJson | DotsJson:
    match rendering:
        case Lines(name=name, strips=strips, style=style):
            return LinesJson(
                name=name,
                strips=[points_of(strip) for strip in strips],
                style=line_style_of(style),
            )
        case Dots(name=name, positions=positions, style=style):
            return DotsJson(
                name=name,
                positions=points_of(positions),
                style=DotStyleJson(color=color_of(style.color), size=style.size),
            )


def entry_of(entry: LegendEntry) -> LegendEntryJson:
    return LegendEntryJson(
        label=entry.label, marks=[mark_of(style) for style in entry.styles]
    )


def mark_of(style: LineStyle | DotStyle) -> LineMarkJson | DotMarkJson:
    match style:
        case LineStyle(color=color, width=width, pattern=pattern):
            return LineMarkJson(color=color_of(color), width=width, pattern=pattern)
        case DotStyle(color=color, size=size):
            return DotMarkJson(color=color_of(color), size=size)


def row_of(row: Row) -> RowJson:
    return RowJson(label=row.label, value=finite(row.value), unit=row.unit or "")


def chart_of(chart: Chart) -> ChartJson:
    return ChartJson(
        id=chart.id,
        title=chart.title,
        y_label=chart.y_label,
        scale=chart.scale,
        lines=[
            ChartLineJson(
                name=line.name,
                values=values_of(line.values),
                style=line_style_of(line.style),
            )
            for line in chart.lines
        ],
    )


def line_style_of(style: LineStyle) -> LineStyleJson:
    return LineStyleJson(
        color=color_of(style.color), width=style.width, pattern=style.pattern
    )


def points_of(points: Points) -> PointsJson:
    return cast(PointsJson, rounded(points).tolist())


def values_of(values: Float[Array, " N"]) -> list[float]:
    return cast(list[float], rounded(values).tolist())


def rounded(values: Array) -> Array:
    array = np.round(np.asarray(values, dtype=float), DECIMALS)
    assert np.all(np.isfinite(array)), (
        "Expected every coordinate and value of the animation to be finite, "
        f"but found {array[~np.isfinite(array)][:3].tolist()}."
    )
    return array


def finite(value: float) -> float:
    assert math.isfinite(value), (
        f"Expected every info value of the animation to be finite, but found {value}."
    )
    return value


def color_of(color: Color) -> ColorJson:
    return (color.red, color.green, color.blue, color.alpha)
