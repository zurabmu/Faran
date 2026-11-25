from dataclasses import dataclass, field

import numpy as np

from faran_visualizer import Rendering, render

from .arrays import Position
from .config import NAVIGATION_CONFIG


@dataclass(frozen=True)
class TrailPoint:
    x: float
    y: float
    step: int


@dataclass
class Trail:
    """The path the unicycle traveled. A point fades out over the trail lifetime, in
    planner steps, after the step that added it."""

    points: list[TrailPoint] = field(default_factory=list)

    @property
    def fading(self) -> bool:
        return len(self.points) > 1

    def extend(self, *, start: Position, end: Position, step: int) -> None:
        """Adds the segment from `start` to `end` that the unicycle traveled in `step`."""
        if not self.points:
            self.points.append(trail_point(start, step=step))
        self.points.append(trail_point(end, step=step))

    def forget_faded(self, *, now: int) -> None:
        """Removes the points that have faded out completely at step `now`."""
        self.points = [
            it
            for it in self.points
            if age(it, now=now) < NAVIGATION_CONFIG.trail_lifetime
        ]

    def settled_renderings(self, *, now: int, growing: bool) -> list[Rendering]:
        """Returns the segments as they look at step `now`, without the newest segment
        when the trail is `growing`."""
        settled = self.points[:-1] if growing else self.points
        return [
            segment_rendering(start, end, index=index, now=now)
            for index, (start, end) in enumerate(zip(settled, settled[1:]))
        ]

    def head_renderings(self, position: Position) -> list[Rendering]:
        """Returns the newest segment, drawn up to the unicycle at `position`."""
        step_start = self.points[-2]
        return [
            render.lines(
                name="trail-head",
                label="Traveled path",
                strips=[np.array([[step_start.x, step_start.y], position])],
                color=NAVIGATION_CONFIG.taken_color,
                width=2.0,
            )
        ]


def trail_point(position: Position, *, step: int) -> TrailPoint:
    x, y = position.tolist()
    return TrailPoint(x=x, y=y, step=step)


def segment_rendering(
    start: TrailPoint, end: TrailPoint, *, index: int, now: int
) -> Rendering:
    return render.lines(
        name=f"trail-{index}",
        label="Traveled path",
        strips=[np.array([[start.x, start.y], [end.x, end.y]])],
        color=f"{NAVIGATION_CONFIG.taken_color}{visibility_byte(age(end, now=now)):02x}",
        width=2.0,
    )


def age(point: TrailPoint, *, now: int) -> int:
    return now - point.step


def visibility_byte(age: int) -> int:
    return round(255 * max(0.0, 1.0 - age / NAVIGATION_CONFIG.trail_lifetime))
