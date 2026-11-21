from typing import Final
import math

from faran_visualizer.renderers.rerun.entities import entities
from faran_visualizer.renderers.rerun.scales import plotted_values
from faran_visualizer.renderers.rerun.timeline import Timeline
from faran_visualizer.scene import Chart, Animation, PlotLine

import rerun as rr

DOTS_PER_CHART: Final = 50
DOT_SIZE_PER_WIDTH: Final = 1.5


def log_charts(
    stream: rr.RecordingStream, animation: Animation, *, timeline: Timeline
) -> None:
    for chart in animation.charts:
        for index, line in enumerate(chart.lines):
            log_line(
                stream,
                line,
                entity=entities.line(chart.id, index=index),
                chart=chart,
                timeline=timeline,
            )


def log_line(
    stream: rr.RecordingStream,
    line: PlotLine,
    *,
    entity: str,
    chart: Chart,
    timeline: Timeline,
) -> None:
    spacing = step_spacing_of(line, step_count=timeline.step_count)
    stream.log(entity, style_of(line), static=True)
    stream.send_columns(
        entity,
        indexes=timeline.columns(timeline.steps[::spacing]),
        columns=rr.Scalars.columns(
            scalars=plotted_values(line.values, chart=chart)[::spacing]
        ),
    )


def style_of(line: PlotLine) -> rr.SeriesLines | rr.SeriesPoints:
    match line.style.pattern:
        case "solid":
            return rr.SeriesLines(
                colors=tuple(line.style.color),
                widths=line.style.width,
                names=line.name,
            )
        case "dashed" | "dotted":
            return rr.SeriesPoints(
                colors=tuple(line.style.color),
                markers="circle",
                marker_sizes=line.style.width * DOT_SIZE_PER_WIDTH,
                names=line.name,
            )


def step_spacing_of(line: PlotLine, *, step_count: int) -> int:
    match line.style.pattern:
        case "solid":
            return 1
        case "dashed" | "dotted":
            return max(1, math.ceil(step_count / DOTS_PER_CHART))
