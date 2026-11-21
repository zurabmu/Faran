from faran_visualizer.driving.styles import Marker, Stroke, styles
from faran_visualizer.scene import Rendering, Points


def optimal_plan(positions: Points) -> list[Rendering]:
    return plan(
        positions,
        name="plans/optimal",
        line=styles.optimal_plan,
        points=styles.optimal_plan_points,
    )


def nominal_plan(positions: Points) -> list[Rendering]:
    return plan(
        positions,
        name="plans/nominal",
        line=styles.nominal_plan,
        points=styles.nominal_plan_points,
    )


def plan(
    positions: Points, *, name: str, line: Stroke, points: Marker
) -> list[Rendering]:
    return [
        line.lines(name=name, strips=[positions]),
        points.dots(name=f"{name}/points", positions=positions),
    ]
