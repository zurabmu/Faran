from collections.abc import Sequence
from typing import Final

import numpy as np

from faran import ExplicitBoundary, Trajectory
from faran.numpy import types
from faran_visualizer import DrivingGeometry, Points, Poses, Rendering, Sizes, render

from .config import CONFIG
from .theme import dusk

type Point = tuple[float, float]
type Reference = Trajectory[types.PathParameters, types.ReferencePoints]

GEOMETRY: Final = DrivingGeometry.create()
SIZES: Final = Sizes(
    wheelbase=CONFIG.vehicle_length,
    vehicle_width=CONFIG.vehicle_width,
    vehicle_radius=None,
    obstacle_radius=CONFIG.circle_radius,
)
VEHICLE: Final = GEOMETRY.vehicle_shape("car", sizes=SIZES)
OBSTACLE_CIRCLE: Final = GEOMETRY.obstacle_shape("circle", sizes=SIZES)


def scene_of(
    reference: Reference,
    *,
    corridor: Sequence[Rendering],
    obstacles: Sequence[Rendering],
) -> list[Rendering]:
    """The parts of a demo that do not move, in meters, in the colors of the site."""
    return [reference_path(reference), *corridor, *obstacles]


def corridor_of(walls: ExplicitBoundary) -> list[Rendering]:
    return [
        render.lines(
            name="boundaries",
            label="Corridor boundaries",
            strips=[np.asarray(walls.left()), np.asarray(walls.right())],
            color=dusk.boundaries,
            width=1.0,
            pattern="dashed",
        )
    ]


def no_corridor() -> list[Rendering]:
    return []


def obstacle_circles(
    *, positions: Sequence[Point], headings: Sequence[float]
) -> list[Rendering]:
    """The circles that approximate each obstacle, as the collision cost sees them."""
    return [
        render.lines(
            name="obstacles",
            label="Obstacles",
            strips=list(OBSTACLE_CIRCLE.outlines(circle_poses(positions, headings))),
            color=dusk.obstacles,
            width=2.0,
        )
    ]


def moving_parts(
    *, driven: Points, plan: Points, x: float, y: float, heading: float
) -> list[Rendering]:
    """The path the vehicle drove, its plan and its body, in meters."""
    return [
        render.lines(
            name="ego/path",
            label="Traveled path",
            strips=[driven],
            color=dusk.traveled_path,
            width=2.0,
        ),
        render.lines(
            name="plans/optimal",
            label="Optimal plan",
            strips=[plan],
            color=dusk.optimal_plan,
            width=2.0,
            pattern="dashed",
        ),
        render.lines(
            name="ego/body",
            label="Ego vehicle",
            strips=list(
                VEHICLE.outlines(
                    Poses(x=np.array([x]), y=np.array([y]), heading=np.array([heading]))
                )
            ),
            color=dusk.ego,
            width=2.0,
        ),
    ]


def reference_path(reference: Reference) -> Rendering:
    return render.lines(
        name="reference",
        label="Reference path",
        strips=[
            GEOMETRY.samples_of(reference, sample_count=CONFIG.reference_sample_count)
        ],
        color=dusk.reference,
        width=2.0,
        pattern="dotted",
    )


def circle_poses(positions: Sequence[Point], headings: Sequence[float]) -> Poses:
    offsets = np.asarray(CONFIG.circle_offsets)
    x, y = np.asarray(positions, dtype=float).T
    angles = np.asarray(headings, dtype=float)
    return Poses(
        x=(x[:, None] + offsets[None, :] * np.cos(angles)[:, None]).ravel(),
        y=(y[:, None] + offsets[None, :] * np.sin(angles)[:, None]).ravel(),
        heading=np.repeat(angles, len(offsets)),
    )
