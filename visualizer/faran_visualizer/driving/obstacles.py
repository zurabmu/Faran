from typing import Final

from faran_visualizer.driving.geometry import Strips, heading_lines, points_from
from faran_visualizer.driving.shapes import Poses, Shape
from faran_visualizer.driving.styles import styles
from faran_visualizer.scene import Points, Rendering

import numpy as np

OBSERVATION_HEADING_LENGTH: Final = 0.3


def obstacle_bodies(poses: Poses, *, shape: Shape) -> list[Rendering]:
    return [
        styles.obstacle.lines(
            name="obstacles/bodies", strips=list(shape.outlines(poses))
        ),
        styles.obstacle_heading.lines(
            name="obstacles/headings", strips=list(shape.heading_lines(poses))
        ),
    ]


def forecasts(paths: list[Points]) -> list[Rendering]:
    return [
        styles.forecast.lines(name="obstacles/forecasts", strips=paths),
        styles.forecast_points.dots(
            name="obstacles/forecasts/points",
            positions=np.concatenate([np.empty((0, 2)), *paths], axis=0),
        ),
    ]


def uncertainties(ellipses: Strips) -> Rendering:
    return styles.uncertainty.lines(
        name="obstacles/uncertainties", strips=list(ellipses)
    )


def observations(poses: Poses) -> list[Rendering]:
    return [
        styles.observation.dots(
            name="obstacles/observations", positions=points_from(poses.x, poses.y)
        ),
        styles.observation_heading.lines(
            name="obstacles/observations/headings",
            strips=list(
                heading_lines(
                    x=poses.x,
                    y=poses.y,
                    heading=poses.heading,
                    length=OBSERVATION_HEADING_LENGTH,
                )
            ),
        ),
    ]
