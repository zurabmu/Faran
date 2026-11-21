from dataclasses import dataclass

from faran import ReferencePoints, Trajectory, types

from faran_visualizer.array import Array
from faran_visualizer.data import Road, Types
from faran_visualizer.driving.geometry import (
    Strips,
    closed_band,
    covariance_ellipses,
    finite,
    offset_curve,
    points_from,
)
from faran_visualizer.driving.shapes import (
    Circle,
    Poses,
    Shape,
    Sizes,
    box_from,
    required,
)
from faran_visualizer.scene import LinePattern, Points

from jaxtyping import Float

import numpy as np

type Reference = Trajectory[types.numpy.PathParameters, ReferencePoints]

MARKING_PATTERNS: dict[Types.Marking, LinePattern] = {
    "solid": "solid",
    "dashed": "dashed",
}


@dataclass(kw_only=True, frozen=True)
class DrivingGeometry:
    """Computes the positions and outlines that a driving simulation shows.

    Attributes:
        confidence_scale: The length of the semi-axes of uncertainty ellipses, in
            standard deviations.
    """

    confidence_scale: float

    @staticmethod
    def create(*, confidence_scale: float = 2.0) -> "DrivingGeometry":
        return DrivingGeometry(confidence_scale=confidence_scale)

    def traveled_positions(
        self, *, x: Float[Array, " T"], y: Float[Array, " T"], step: int
    ) -> Points:
        """Returns the positions from the first step up to and including `step`."""
        return points_from(x[: step + 1], y[: step + 1])

    def positions_on(
        self, reference: Reference, *, path_parameters: Float[Array, " N"]
    ) -> Points:
        """Returns the positions on the reference at the path parameters."""
        points = reference.query(
            types.numpy.path_parameters(path_parameters.reshape(-1, 1))
        )
        return points_from(np.asarray(points.x())[:, 0], np.asarray(points.y())[:, 0])

    def samples_of(self, reference: Reference, *, sample_count: int) -> Points:
        """Returns `sample_count` evenly spaced positions along the whole reference."""
        return self.positions_on(
            reference,
            path_parameters=np.linspace(0, reference.path_length, sample_count),
        )

    def vehicle_shape(self, vehicle_type: Types.Vehicle, *, sizes: Sizes) -> Shape:
        match vehicle_type:
            case "circle":
                return Circle(
                    radius=required(
                        sizes.vehicle_radius,
                        name="vehicle_radius",
                        rendered="the ego vehicle",
                    )
                )
            case "triangle" | "car":
                return box_from(sizes, rendered="the ego vehicle")

    def obstacle_shape(
        self, obstacle_shape: Types.ObstacleShape, *, sizes: Sizes
    ) -> Shape:
        match obstacle_shape:
            case "circle":
                return Circle(
                    radius=required(
                        sizes.obstacle_radius,
                        name="obstacle_radius",
                        rendered="obstacles",
                    )
                )
            case "rectangle":
                return box_from(sizes, rendered="obstacles")

    def present(
        self,
        *,
        x: Float[Array, " K"],
        y: Float[Array, " K"],
        heading: Float[Array, " K"],
    ) -> Poses:
        """Returns the poses that have a finite position and heading."""
        is_present = finite(x, y, heading)
        return Poses(x=x[is_present], y=y[is_present], heading=heading[is_present])

    def forecast_paths(
        self, *, x: Float[Array, "H K"], y: Float[Array, "H K"]
    ) -> list[Points]:
        """Returns one path per obstacle, without the points that are not finite."""
        paths = np.stack([x, y], axis=-1).swapaxes(0, 1)
        return [path[finite(path[:, 0], path[:, 1])] for path in paths]

    def uncertainty_ellipses(
        self,
        *,
        x: Float[Array, "H K"],
        y: Float[Array, "H K"],
        covariance: Float[Array, "H D D K"],
    ) -> Strips:
        """Returns the confidence ellipse of each forecast position with a finite
        position and covariance. The first two state dimensions of the covariance
        are the position."""
        centers = np.stack([x, y], axis=-1).reshape(-1, 2)
        covariances = np.moveaxis(covariance[:, :2, :2, :], -1, 1).reshape(-1, 2, 2)
        is_present = finite(centers[:, 0], centers[:, 1]) & np.isfinite(
            covariances
        ).all(axis=(1, 2))
        return covariance_ellipses(
            centers=centers[is_present],
            covariances=covariances[is_present],
            confidence_scale=self.confidence_scale,
        )

    def lane_surface(self, lane: Road.Lane) -> Points:
        """Returns the closed outline of the lane between its boundaries."""
        left, right = edges_of(lane)
        return closed_band(left=left, right=right)

    def marked_edges(self, network: Road.Network) -> dict[LinePattern, list[Points]]:
        """Returns the marked lane edges, grouped by the pattern their marking is
        rendered with. Unmarked edges are left out."""
        return {
            pattern: [
                edge
                for lane in network.lanes
                for marking, edge in zip(lane.markings, edges_of(lane))
                if MARKING_PATTERNS.get(marking) == pattern
            ]
            for pattern in MARKING_PATTERNS.values()
        }


def edges_of(lane: Road.Lane) -> tuple[Points, Points]:
    center = points_from(lane.x, lane.y)
    left_width, right_width = lane.boundaries
    return (
        offset_curve(center, distance=left_width),
        offset_curve(center, distance=-right_width),
    )
