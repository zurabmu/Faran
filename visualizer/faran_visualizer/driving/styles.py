from typing import Sequence
from dataclasses import dataclass

from faran_visualizer.scene import Rendering, LinePattern, Points, render
from faran_visualizer.theme import Theme


@dataclass(kw_only=True, frozen=True)
class Stroke:
    color: str
    width: float
    pattern: LinePattern = "solid"

    def lines(self, *, name: str, label: str, strips: Sequence[Points]) -> Rendering:
        return render.lines(
            name=name,
            label=label,
            strips=strips,
            color=self.color,
            width=self.width,
            pattern=self.pattern,
        )


@dataclass(kw_only=True, frozen=True)
class Marker:
    color: str
    size: float

    def dots(self, *, name: str, label: str, positions: Points) -> Rendering:
        return render.dots(
            name=name,
            label=label,
            positions=positions,
            color=self.color,
            size=self.size,
        )


@dataclass(kw_only=True, frozen=True)
class Styles:
    """How each part of a driving scene is drawn."""

    road_surface: Stroke
    lane_marking: Stroke
    reference: Stroke
    boundary: Stroke
    traveled_path: Stroke
    ego: Stroke
    ego_heading: Stroke
    ghost: Marker
    optimal_plan: Stroke
    optimal_plan_points: Marker
    nominal_plan: Stroke
    nominal_plan_points: Marker
    obstacle: Stroke
    obstacle_heading: Stroke
    observation: Marker
    observation_heading: Stroke
    forecast: Stroke
    forecast_points: Marker
    uncertainty: Stroke

    @staticmethod
    def of(theme: Theme) -> "Styles":
        """Returns the styles that draw a driving scene in the colors of the theme."""
        return Styles(
            road_surface=Stroke(color=theme.road, width=1.0),
            lane_marking=Stroke(color=theme.lane_markings, width=2.0),
            reference=Stroke(color=theme.reference, width=2.0, pattern="dotted"),
            boundary=Stroke(color=theme.boundaries, width=1.0, pattern="dashed"),
            traveled_path=Stroke(color=theme.traveled_path, width=2.0),
            ego=Stroke(color=theme.ego, width=2.0),
            ego_heading=Stroke(color=theme.ego_heading, width=3.0),
            ghost=Marker(color=theme.ghost, size=12.0),
            optimal_plan=Stroke(color=theme.optimal_plan, width=2.0, pattern="dashed"),
            optimal_plan_points=Marker(color=theme.optimal_plan, size=5.0),
            nominal_plan=Stroke(color=theme.nominal_plan, width=2.0),
            nominal_plan_points=Marker(color=theme.nominal_plan, size=5.0),
            obstacle=Stroke(color=theme.obstacles, width=2.0),
            obstacle_heading=Stroke(color=theme.obstacle_headings, width=3.0),
            observation=Marker(color=theme.observations, size=5.0),
            observation_heading=Stroke(color=theme.observation_headings, width=2.0),
            forecast=Stroke(color=theme.forecasts, width=2.0),
            forecast_points=Marker(color=theme.forecasts, size=4.0),
            uncertainty=Stroke(color=theme.uncertainties, width=1.0),
        )
