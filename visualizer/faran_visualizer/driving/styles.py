from typing import Final, Sequence
from dataclasses import dataclass

from faran_visualizer.scene import Rendering, LinePattern, Points, render


@dataclass(kw_only=True, frozen=True)
class Stroke:
    color: str
    width: float
    pattern: LinePattern = "solid"

    def lines(self, *, name: str, strips: Sequence[Points]) -> Rendering:
        return render.lines(
            name=name,
            strips=strips,
            color=self.color,
            width=self.width,
            pattern=self.pattern,
        )


@dataclass(kw_only=True, frozen=True)
class Marker:
    color: str
    size: float

    def dots(self, *, name: str, positions: Points) -> Rendering:
        return render.dots(
            name=name, positions=positions, color=self.color, size=self.size
        )


class styles:
    road_surface: Final = Stroke(color="#8a8a8a80", width=1.0)
    lane_marking: Final = Stroke(color="#00e5ff54", width=2.0)
    reference: Final = Stroke(color="#bdc3c7", width=2.0, pattern="dashed")
    boundary: Final = Stroke(color="#ffa200", width=1.0, pattern="dashed")
    traveled_path: Final = Stroke(color="#3498db", width=2.0)
    ego: Final = Stroke(color="#e74c3c", width=2.0)
    ego_heading: Final = Stroke(color="#c0392b", width=3.0)
    ghost: Final = Marker(color="#2ecc7180", size=12.0)
    optimal_plan: Final = Stroke(color="#e63946cc", width=2.0)
    optimal_plan_points: Final = Marker(color="#e63946cc", size=5.0)
    nominal_plan: Final = Stroke(color="#2a9d8fcc", width=2.0)
    nominal_plan_points: Final = Marker(color="#2a9d8fcc", size=5.0)
    obstacle: Final = Stroke(color="#7f8c8de6", width=2.0)
    obstacle_heading: Final = Stroke(color="#5a6263", width=3.0)
    observation: Final = Marker(color="#3498db", size=5.0)
    observation_heading: Final = Stroke(color="#2980b9", width=2.0)
    forecast: Final = Stroke(color="#9b59b699", width=2.0)
    forecast_points: Final = Marker(color="#9b59b699", size=4.0)
    uncertainty: Final = Stroke(color="#9b59b666", width=1.0)
