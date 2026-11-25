from typing import Final

from faran_visualizer import Theme

dusk: Final = Theme(
    background="#0f0d17",
    lines=(
        "#a3a6ff",
        "#ffa487",
        "#8fd3c4",
        "#d3a6f0",
        "#ffd2c2",
        "#8fbde0",
        "#f2a0bf",
        "#b0b9ee",
    ),
    bands="#7f83f0",
    road="#3e365080",
    lane_markings="#b8afc640",
    reference="#f1e4ecaa",
    boundaries="#f08a6a",
    traveled_path="#ffa487",
    ego="#ffa487",
    ego_heading="#ffd2c2",
    ghost="#f1e4ec80",
    optimal_plan="#a3a6ffdd",
    nominal_plan="#7f83f088",
    obstacles="#b8afc6e6",
    obstacle_headings="#f1ecf4",
    observations="#b0b9ee",
    observation_headings="#a3a6ff",
    forecasts="#d3a6f099",
    uncertainties="#d3a6f066",
)
"""The colors of the documentation site, for the replays of the examples."""
