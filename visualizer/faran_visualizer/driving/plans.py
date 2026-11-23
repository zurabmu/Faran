from faran_visualizer.driving.styles import Marker, Stroke, Styles
from faran_visualizer.scene import Rendering, Points


def optimal_plan(positions: Points, *, styles: Styles) -> list[Rendering]:
    return plan(
        positions,
        name="plans/optimal",
        label="Optimal plan",
        line=styles.optimal_plan,
        points=styles.optimal_plan_points,
    )


def nominal_plan(positions: Points, *, styles: Styles) -> list[Rendering]:
    return plan(
        positions,
        name="plans/nominal",
        label="Nominal plan",
        line=styles.nominal_plan,
        points=styles.nominal_plan_points,
    )


def plan(
    positions: Points, *, name: str, label: str, line: Stroke, points: Marker
) -> list[Rendering]:
    return [
        line.lines(name=name, label=label, strips=[positions]),
        points.dots(name=f"{name}/points", label=label, positions=positions),
    ]
