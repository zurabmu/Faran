from typing import Sequence

from faran_visualizer.array import Array
from faran_visualizer.data import Plot, Plots, plots_in
from faran_visualizer.scene.colors import color, line_color
from faran_visualizer.scene.animation import Chart, Color, LineStyle, PlotLine
from faran_visualizer.scene.styles import styles

from jaxtyping import Float

import numpy as np


def charts_from(plots: Plots, *, step_count: int) -> list[Chart]:
    """Returns one chart per entry: a plot gets a chart of its own, and a
    `Plot.Chart` renders all of its plots in one chart."""
    return [
        chart_of(entry, chart_id=str(index), step_count=step_count)
        for index, entry in enumerate(plots)
    ]


def chart_of(entry: Plot | Plot.Chart, *, chart_id: str, step_count: int) -> Chart:
    plots = plots_in(entry)
    line_offsets = np.cumsum([0, *(len(plot.lines) for plot in plots)])
    return Chart(
        id=chart_id,
        title=entry.name,
        y_label=axis_label(entry.name, unit=entry.unit),
        scale=entry.scale,
        lines=[
            line
            for plot, offset in zip(plots, line_offsets)
            for line in lines_of(plot, line_offset=int(offset), step_count=step_count)
        ],
    )


def lines_of(plot: Plot, *, line_offset: int, step_count: int) -> list[PlotLine]:
    guide_color = line_color(
        plot.lines[0].color if plot.lines else None, index=line_offset
    )
    return [
        *(
            PlotLine(
                name=line.label,
                values=line.values,
                style=LineStyle(
                    color=line_color(line.color, index=line_offset + index),
                    width=styles.line_width,
                ),
            )
            for index, line in enumerate(plot.lines)
        ),
        *(
            bound_line(bound, color=guide_color, step_count=step_count)
            for bound in plot.bounds
        ),
        *(line for band in plot.bands for line in band_lines(band)),
    ]


def bound_line(bound: Plot.Bound, *, color: Color, step_count: int) -> PlotLine:
    return PlotLine(
        name=bound.label,
        values=broadcast(bound.values, step_count=step_count),
        style=LineStyle(color=color, width=styles.guide_width, pattern="dotted"),
    )


def band_lines(band: Plot.Band) -> Sequence[PlotLine]:
    style = LineStyle(
        color=color(
            band.color if band.color is not None else styles.band_color,
            alpha=styles.band_alpha,
        ),
        width=styles.guide_width,
    )
    return [
        PlotLine(name=band.lower_name, values=band.lower, style=style),
        PlotLine(name=band.upper_name, values=band.upper, style=style),
    ]


def broadcast(
    values: Float[Array, " T"] | float, *, step_count: int
) -> Float[Array, " T"]:
    return np.broadcast_to(np.asarray(values, dtype=float), (step_count,))


def axis_label(name: str, *, unit: str | None) -> str:
    return name if unit is None else f"{name} ({unit})"
