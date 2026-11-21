from typing import Final

from faran_visualizer.array import Array
from faran_visualizer.scene import Points

from jaxtyping import Bool, Float

import numpy as np

ELLIPSE_SEGMENT_COUNT: Final = 36
MINIMUM_TANGENT_LENGTH: Final = 1e-10

UNIT_SQUARE: Final = np.array(
    [[-0.5, -0.5], [0.5, -0.5], [0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5]]
)

UNIT_CIRCLE: Final = np.stack(
    [
        np.cos(angles := np.linspace(0, 2 * np.pi, ELLIPSE_SEGMENT_COUNT + 1)),
        np.sin(angles),
    ],
    axis=-1,
)

type Strips = Float[Array, "K P 2"]
"""K line strips with P points each."""


def points_from(x: Float[Array, " N"], y: Float[Array, " N"]) -> Points:
    return np.stack([np.asarray(x, dtype=float), np.asarray(y, dtype=float)], axis=-1)


def finite(*arrays: Float[Array, " N"]) -> Bool[Array, " N"]:
    """Returns a mask that is true where every given array has a finite value."""
    return np.logical_and.reduce([np.isfinite(it) for it in arrays])


def boxes(
    *,
    x: Float[Array, " N"],
    y: Float[Array, " N"],
    heading: Float[Array, " N"],
    length: float,
    width: float,
) -> Strips:
    """Returns closed outlines of rectangles centered at (x, y), with `length`
    along the heading."""
    corners = UNIT_SQUARE * np.array([length, width])
    return (
        np.einsum("kij,pj->kpi", rotations(heading), corners)
        + points_from(x, y)[:, None, :]
    )


def circles(*, x: Float[Array, " N"], y: Float[Array, " N"], radius: float) -> Strips:
    return points_from(x, y)[:, None, :] + radius * UNIT_CIRCLE


def heading_lines(
    *,
    x: Float[Array, " N"],
    y: Float[Array, " N"],
    heading: Float[Array, " N"],
    length: float,
) -> Strips:
    """Returns line segments that start at (x, y) and point along the heading."""
    starts = points_from(x, y)
    ends = starts + length * np.stack([np.cos(heading), np.sin(heading)], axis=-1)
    return np.stack([starts, ends], axis=1)


def covariance_ellipses(
    *, centers: Points, covariances: Float[Array, "N 2 2"], confidence_scale: float
) -> Strips:
    """Returns closed outlines of the confidence ellipses of position
    covariances. The semi-axes are `confidence_scale` standard deviations long."""
    variances, directions = np.linalg.eigh(symmetric(covariances))
    semi_axes = directions * np.sqrt(np.maximum(variances, 0.0))[:, None, :]
    return centers[:, None, :] + confidence_scale * np.einsum(
        "nij,pj->npi", semi_axes, UNIT_CIRCLE
    )


def offset_curve(points: Points, *, distance: float) -> Points:
    """Returns the polyline moved by `distance` along its left normal. A negative
    distance moves it to the right."""
    return points + distance * left_normals(points)


def closed_band(*, left: Points, right: Points) -> Points:
    """Returns the closed outline of the area between two polylines of equal length."""
    return np.concatenate([left, right[::-1], left[:1]], axis=0)


def rotations(headings: Float[Array, " N"]) -> Float[Array, "N 2 2"]:
    cosines, sines = np.cos(headings), np.sin(headings)
    return np.stack(
        [np.stack([cosines, -sines], axis=-1), np.stack([sines, cosines], axis=-1)],
        axis=-2,
    )


def symmetric(matrices: Float[Array, "N 2 2"]) -> Float[Array, "N 2 2"]:
    return (matrices + np.swapaxes(matrices, -1, -2)) / 2


def left_normals(points: Points) -> Points:
    tangents: Points = np.asarray(np.gradient(points, axis=0))
    lengths = np.linalg.norm(tangents, axis=-1, keepdims=True)
    normals = np.stack([-tangents[:, 1], tangents[:, 0]], axis=-1)
    return np.where(
        lengths > MINIMUM_TANGENT_LENGTH,
        normals / np.maximum(lengths, MINIMUM_TANGENT_LENGTH),
        np.array([0.0, 1.0]),
    )
