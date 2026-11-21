from typing import Protocol
from dataclasses import dataclass

from faran_visualizer.array import Array
from faran_visualizer.driving.geometry import Strips, boxes, circles, heading_lines

from jaxtyping import Float

import numpy as np


@dataclass(kw_only=True, frozen=True)
class Poses:
    x: Float[Array, " N"]
    y: Float[Array, " N"]
    heading: Float[Array, " N"]


class Shape(Protocol):
    def outlines(self, poses: Poses) -> Strips:
        """Returns one closed outline per pose."""
        ...

    def heading_lines(self, poses: Poses) -> Strips:
        """Returns the line segments that mark the heading of shapes whose outline
        does not show it. Shapes that show their heading return no segments."""
        ...


@dataclass(kw_only=True, frozen=True)
class Box:
    length: float
    width: float

    def outlines(self, poses: Poses) -> Strips:
        return boxes(
            x=poses.x,
            y=poses.y,
            heading=poses.heading,
            length=self.length,
            width=self.width,
        )

    def heading_lines(self, poses: Poses) -> Strips:
        return np.empty((0, 2, 2))


@dataclass(kw_only=True, frozen=True)
class Circle:
    radius: float

    def outlines(self, poses: Poses) -> Strips:
        return circles(x=poses.x, y=poses.y, radius=self.radius)

    def heading_lines(self, poses: Poses) -> Strips:
        return heading_lines(
            x=poses.x, y=poses.y, heading=poses.heading, length=self.radius
        )


@dataclass(kw_only=True, frozen=True)
class Sizes:
    """The sizes of the rendered vehicles, in meters, as a simulation result gives them."""

    wheelbase: float | None
    vehicle_width: float | None
    vehicle_radius: float | None
    obstacle_radius: float | None


def box_from(sizes: Sizes, *, rendered: str) -> Box:
    return Box(
        length=required(sizes.wheelbase, name="wheelbase", rendered=rendered),
        width=required(sizes.vehicle_width, name="vehicle_width", rendered=rendered),
    )


def required(value: float | None, *, name: str, rendered: str) -> float:
    assert value is not None, (
        f"MpccSimulationResult.{name} is required to render {rendered} with the chosen "
        f"shape, but it is None."
    )
    return value
