from typing import Final, Sequence
from dataclasses import dataclass
import math

from faran_visualizer.renderers.rerun.entities import entities
from faran_visualizer.renderers.rerun.renderings import radius_of
from faran_visualizer.scene import (
    Animation,
    Color,
    DotStyle,
    LegendEntry,
    LinePattern,
    LineStyle,
)

import rerun as rr

MAXIMUM_COLUMNS: Final = 3
CELL_WIDTH: Final = 4.0
CELL_HEIGHT: Final = 1.5
SAMPLE_LENGTH: Final = 2.0
TOP_MARGIN: Final = 0.5
LABEL_HEIGHT: Final = 1.0
DARK_TEXT: Final = (24, 22, 30, 255)
LIGHT_TEXT: Final = (236, 232, 240, 255)
LIGHT_BACKGROUND_LUMINANCE: Final = 0.5

type Segment = list[tuple[float, float]]


@dataclass(kw_only=True, frozen=True)
class Cell:
    x: float
    y: float

    @staticmethod
    def at(index: int, *, columns: int) -> "Cell":
        row, column = divmod(index, columns)
        return Cell(x=(column + 0.5) * CELL_WIDTH, y=row * CELL_HEIGHT)


def legend_rows(legend: Sequence[LegendEntry]) -> int:
    """Returns the number of rows the legend takes in its view."""
    return math.ceil(len(legend) / columns_for(legend))


def legend_bounds(legend: Sequence[LegendEntry]) -> tuple[list[float], list[float]]:
    """Returns the x and y ranges that show every entry of the legend."""
    return (
        [0.0, columns_for(legend) * CELL_WIDTH],
        [-TOP_MARGIN, (legend_rows(legend) - 1) * CELL_HEIGHT + LABEL_HEIGHT],
    )


def log_legend(stream: rr.RecordingStream, animation: Animation) -> None:
    columns = columns_for(animation.legend)
    text = label_color(animation.background_color)
    for index, entry in enumerate(animation.legend):
        cell = Cell.at(index, columns=columns)
        for order, style in enumerate(entry.styles):
            stream.log(
                entities.legend_sample(index, index=order),
                sample_of(style, cell=cell),
                static=True,
            )
        stream.log(
            entities.legend_label(index),
            rr.Points2D(
                [(cell.x, cell.y)],
                radii=0.0,
                colors=text,
                labels=[entry.label],
                show_labels=True,
            ),
            static=True,
        )


def columns_for(legend: Sequence[LegendEntry]) -> int:
    return max(1, min(MAXIMUM_COLUMNS, len(legend)))


def label_color(background: Color) -> tuple[int, int, int, int]:
    is_light = luminance_of(background) > LIGHT_BACKGROUND_LUMINANCE
    return DARK_TEXT if is_light else LIGHT_TEXT


def luminance_of(color: Color) -> float:
    return (0.2126 * color.red + 0.7152 * color.green + 0.0722 * color.blue) / 255


def sample_of(
    style: LineStyle | DotStyle, *, cell: Cell
) -> rr.LineStrips2D | rr.Points2D:
    match style:
        case LineStyle(color=color, width=width, pattern=pattern):
            return rr.LineStrips2D(
                segments_of(pattern, cell=cell),
                radii=radius_of(width),
                colors=tuple(color),
            )
        case DotStyle(color=color, size=size):
            return rr.Points2D(
                [(cell.x, cell.y)], radii=radius_of(size), colors=tuple(color)
            )


def segments_of(pattern: LinePattern, *, cell: Cell) -> list[Segment]:
    match pattern:
        case "solid":
            return dashes(dash=SAMPLE_LENGTH, gap=0.0, cell=cell)
        case "dashed":
            return dashes(dash=0.3, gap=0.2, cell=cell)
        case "dotted":
            return dashes(dash=0.06, gap=0.2, cell=cell)


def dashes(*, dash: float, gap: float, cell: Cell) -> list[Segment]:
    start = cell.x - SAMPLE_LENGTH / 2
    count = math.ceil(SAMPLE_LENGTH / (dash + gap))
    offsets = [step * (dash + gap) for step in range(count)]
    return [
        [
            (start + offset, cell.y),
            (start + min(offset + dash, SAMPLE_LENGTH), cell.y),
        ]
        for offset in offsets
    ]
