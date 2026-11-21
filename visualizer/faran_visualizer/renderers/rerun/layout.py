from faran_visualizer.renderers.rerun.entities import entities
from faran_visualizer.renderers.rerun.scales import axis_label
from faran_visualizer.renderers.rerun.timeline import Timeline
from faran_visualizer.scene import Chart, Animation

import rerun.blueprint as rrb


def blueprint_for(animation: Animation, *, timeline: Timeline) -> rrb.Blueprint:
    """Returns the default layout: the scene on the left, and the info table above
    one tab per chart on the right."""
    return rrb.Blueprint(
        rrb.Horizontal(
            rrb.Spatial2DView(
                origin="/", contents=f"/{entities.scene}/**", name="Animation"
            ),
            rrb.Vertical(
                *(rows := [info_view(), *chart_tabs(animation)]),
                row_shares=[1.0, *(3.0 for _ in rows[1:])],
            ),
            column_shares=[3.0, 2.0],
        ),
        rrb.BlueprintPanel(state="collapsed"),
        rrb.SelectionPanel(state="collapsed"),
        timeline.time_panel(),
    )


def info_view() -> rrb.TextDocumentView:
    return rrb.TextDocumentView(origin=f"/{entities.info}", name="Simulation State")


def chart_tabs(animation: Animation) -> list[rrb.Tabs]:
    if len(animation.charts) == 0:
        return []

    return [rrb.Tabs(*(chart_view(chart) for chart in animation.charts))]


def chart_view(chart: Chart) -> rrb.TimeSeriesView:
    return rrb.TimeSeriesView(
        origin=f"/{entities.chart(chart.id)}",
        name=f"{chart.title} · {axis_label(chart)}",
    )
