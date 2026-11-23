from typing import Final

from faran_visualizer.renderers.rerun.entities import entities
from faran_visualizer.renderers.rerun.legend import legend_bounds, legend_rows
from faran_visualizer.renderers.rerun.scales import axis_label
from faran_visualizer.renderers.rerun.timeline import Timeline
from faran_visualizer.scene import Chart, Animation, Color

import rerun.blueprint as rrb

INFO_SHARE: Final = 1.0
CHARTS_SHARE: Final = 3.0
LEGEND_SHARE_PER_ROW: Final = 0.45


def blueprint_for(animation: Animation, *, timeline: Timeline) -> rrb.Blueprint:
    """Returns the default layout: the scene on the left, and the legend and the info
    table above one tab per chart on the right."""
    return rrb.Blueprint(
        rrb.Horizontal(
            rrb.Spatial2DView(
                origin="/",
                contents=f"/{entities.scene}/**",
                name="Animation",
                background=tuple(animation.background_color),
            ),
            rrb.Vertical(
                *legend_views(animation),
                info_view(),
                *chart_tabs(animation),
                row_shares=[
                    *legend_shares(animation),
                    INFO_SHARE,
                    *(CHARTS_SHARE for _ in chart_tabs(animation)),
                ],
            ),
            column_shares=[3.0, 2.0],
        ),
        rrb.BlueprintPanel(state="collapsed"),
        rrb.SelectionPanel(state="collapsed"),
        timeline.time_panel(),
    )


def legend_views(animation: Animation) -> list[rrb.Spatial2DView]:
    if len(animation.legend) == 0:
        return []

    x_range, y_range = legend_bounds(animation.legend)
    return [
        rrb.Spatial2DView(
            origin=f"/{entities.legend}",
            name="Legend",
            background=tuple(animation.background_color),
            visual_bounds=rrb.VisualBounds2D(x_range=x_range, y_range=y_range),
        )
    ]


def legend_shares(animation: Animation) -> list[float]:
    return [
        LEGEND_SHARE_PER_ROW * legend_rows(animation.legend)
        for _ in legend_views(animation)
    ]


def info_view() -> rrb.TextDocumentView:
    return rrb.TextDocumentView(origin=f"/{entities.info}", name="Simulation State")


def chart_tabs(animation: Animation) -> list[rrb.Tabs]:
    if len(animation.charts) == 0:
        return []

    return [
        rrb.Tabs(
            *(
                chart_view(chart, background=animation.background_color)
                for chart in animation.charts
            )
        )
    ]


def chart_view(chart: Chart, *, background: Color) -> rrb.TimeSeriesView:
    return rrb.TimeSeriesView(
        origin=f"/{entities.chart(chart.id)}",
        name=f"{chart.title} · {axis_label(chart)}",
        background=rrb.archetypes.PlotBackground(color=tuple(background)),
    )
