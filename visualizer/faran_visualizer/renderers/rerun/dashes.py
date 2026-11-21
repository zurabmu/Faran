from typing import Final, Sequence
from dataclasses import dataclass

from faran_visualizer.array import Array
from faran_visualizer.scene import Points

from jaxtyping import Float

import numpy as np

SCENE_FRACTION_PER_DASH: Final = 0.01
GAP_FRACTION_OF_DASH: Final = 0.75
DOT_FRACTION_OF_DASH: Final = 0.2
MINIMUM_DASH_LENGTH: Final = 1e-3


@dataclass(kw_only=True, frozen=True)
class DashPattern:
    dash_length: float
    gap_length: float

    @staticmethod
    def dashed_for(scene: Sequence[Points]) -> "DashPattern":
        """Returns dashes whose length is proportional to the size of the area that
        the points cover."""
        dash_length = dash_length_for(scene)
        return DashPattern(
            dash_length=dash_length, gap_length=dash_length * GAP_FRACTION_OF_DASH
        )

    @staticmethod
    def dotted_for(scene: Sequence[Points]) -> "DashPattern":
        dash_length = dash_length_for(scene)
        return DashPattern(
            dash_length=dash_length * DOT_FRACTION_OF_DASH,
            gap_length=dash_length * GAP_FRACTION_OF_DASH,
        )

    def split(self, points: Points) -> list[Points]:
        arc_lengths = arc_lengths_of(points)
        starts = np.arange(0.0, arc_lengths[-1], self.dash_length + self.gap_length)
        return [
            part_between(
                points,
                arc_lengths=arc_lengths,
                start=start,
                end=min(start + self.dash_length, arc_lengths[-1]),
            )
            for start in starts
        ]


def dash_length_for(scene: Sequence[Points]) -> float:
    points = np.concatenate([np.empty((0, 2)), *scene], axis=0)
    finite_points = points[np.isfinite(points).all(axis=1)]

    if len(finite_points) == 0:
        return MINIMUM_DASH_LENGTH

    diagonal = np.linalg.norm(finite_points.max(axis=0) - finite_points.min(axis=0))
    return max(float(diagonal) * SCENE_FRACTION_PER_DASH, MINIMUM_DASH_LENGTH)


def arc_lengths_of(points: Points) -> Float[Array, " N"]:
    segment_lengths = np.linalg.norm(np.diff(points, axis=0), axis=-1)
    return np.concatenate([[0.0], np.cumsum(segment_lengths)])


def part_between(
    points: Points, *, arc_lengths: Float[Array, " N"], start: float, end: float
) -> Points:
    inner = (arc_lengths > start) & (arc_lengths < end)
    samples = np.concatenate([[start], arc_lengths[inner], [end]])
    return np.stack(
        [
            np.interp(samples, arc_lengths, points[:, 0]),
            np.interp(samples, arc_lengths, points[:, 1]),
        ],
        axis=-1,
    )
