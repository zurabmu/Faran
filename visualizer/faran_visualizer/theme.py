from typing import Sequence
from dataclasses import dataclass


@dataclass(kw_only=True, frozen=True)
class Theme:
    """The colors of a visualization. Every color is a hex color (`#rgb`,
    `#rrggbb` or `#rrggbbaa`) or a basic color name, as `render` accepts them.

    Attributes:
        background: The background of the scene and of every chart.
        lines: The colors of plot lines that have no color of their own, used in
            order and repeated when a chart has more lines.
        bands: The color of plot bands that have no color of their own.
        road: The lane surfaces.
        lane_markings: The lane edges.
        reference: The reference path.
        boundaries: The corridor boundaries.
        traveled_path: The path the ego has traveled.
        ego: The outline of the ego.
        ego_heading: The heading line of the ego.
        ghost: The point on the reference path at the ego's path parameter.
        optimal_plan: The optimal plan and its points.
        nominal_plan: The nominal plan and its points.
        obstacles: The outlines of the obstacles.
        obstacle_headings: The heading lines of the obstacles.
        observations: The observed obstacle positions.
        observation_headings: The heading lines of the observed obstacles.
        forecasts: The forecast obstacle paths and their points.
        uncertainties: The uncertainty ellipses of the forecasts.
    """

    background: str
    lines: Sequence[str]
    bands: str
    road: str
    lane_markings: str
    reference: str
    boundaries: str
    traveled_path: str
    ego: str
    ego_heading: str
    ghost: str
    optimal_plan: str
    nominal_plan: str
    obstacles: str
    obstacle_headings: str
    observations: str
    observation_headings: str
    forecasts: str
    uncertainties: str

    @staticmethod
    def default() -> "Theme":
        """Returns the theme visualizations use unless another one is configured."""
        return Theme(
            background="#1c1c1c",
            lines=(
                "#3498db",
                "#e74c3c",
                "#2ecc71",
                "#9b59b6",
                "#f39c12",
                "#1abc9c",
                "#e91e63",
                "#795548",
            ),
            bands="#3498db",
            road="#8a8a8a80",
            lane_markings="#00e5ff54",
            reference="#bdc3c7",
            boundaries="#ffa200",
            traveled_path="#3498db",
            ego="#e74c3c",
            ego_heading="#c0392b",
            ghost="#2ecc7180",
            optimal_plan="#e63946cc",
            nominal_plan="#2a9d8fcc",
            obstacles="#7f8c8de6",
            obstacle_headings="#5a6263",
            observations="#3498db",
            observation_headings="#2980b9",
            forecasts="#9b59b699",
            uncertainties="#9b59b666",
        )
