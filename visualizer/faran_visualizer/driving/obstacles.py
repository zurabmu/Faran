from typing import Final

from faran_visualizer.driving.geometry import Strips, heading_lines, points_from
from faran_visualizer.driving.shapes import Poses, Shape
from faran_visualizer.driving.styles import Styles
from faran_visualizer.scene import Points, Rendering

import numpy as np

OBSERVATION_HEADING_LENGTH: Final = 0.3


def obstacle_bodies(poses: Poses, *, shape: Shape, styles: Styles) -> list[Rendering]:
    return [
        styles.obstacle.lines(
            name="obstacles/bodies",
            label="Obstacles",
            strips=list(shape.outlines(poses)),
        ),
        styles.obstacle_heading.lines(
            name="obstacles/headings",
            label="Obstacles",
            strips=list(shape.heading_lines(poses)),
        ),
    ]


def forecasts(paths: list[Points], *, styles: Styles) -> list[Rendering]:
    return [
        styles.forecast.lines(
            name="obstacles/forecasts", label="Forecasts", strips=paths
        ),
        styles.forecast_points.dots(
            name="obstacles/forecasts/points",
            label="Forecasts",
            positions=np.concatenate([np.empty((0, 2)), *paths], axis=0),
        ),
    ]


def uncertainties(ellipses: Strips, *, styles: Styles) -> Rendering:
    return styles.uncertainty.lines(
        name="obstacles/uncertainties",
        label="Forecast uncertainty",
        strips=list(ellipses),
    )


def observations(poses: Poses, *, styles: Styles) -> list[Rendering]:
    return [
        styles.observation.dots(
            name="obstacles/observations",
            label="Observations",
            positions=points_from(poses.x, poses.y),
        ),
        styles.observation_heading.lines(
            name="obstacles/observations/headings",
            label="Observations",
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
