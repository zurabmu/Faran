from typing import Final
from dataclasses import dataclass

from faran_visualizer.renderers.rerun.dashes import DashPattern
from faran_visualizer.renderers.rerun.entities import entities
from faran_visualizer.renderers.rerun.timeline import Timeline
from faran_visualizer.scene import Animation, Dots, Rendering, Lines, Points

import numpy.typing as npt
import rerun as rr

FRAME_DRAW_ORDER_OFFSET: Final = 1000.0


@dataclass(kw_only=True, frozen=True)
class Patterns:
    dashed: DashPattern
    dotted: DashPattern

    @staticmethod
    def for_animation(animation: Animation) -> "Patterns":
        points = [
            strip
            for rendering in animation.background
            if isinstance(rendering, Lines)
            for strip in rendering.strips
        ]
        return Patterns(
            dashed=DashPattern.dashed_for(points), dotted=DashPattern.dotted_for(points)
        )

    def strips(self, lines: Lines) -> list[Points]:
        match lines.style.pattern:
            case "solid":
                return list(lines.strips)
            case "dashed":
                return [
                    dash for strip in lines.strips for dash in self.dashed.split(strip)
                ]
            case "dotted":
                return [
                    dot for strip in lines.strips for dot in self.dotted.split(strip)
                ]


def log_scene_frame(stream: rr.RecordingStream) -> None:
    """Flips the scene so the y axis points up in the 2D view. Logged positions keep
    their values."""
    stream.log(entities.scene, rr.Transform3D(scale=[1.0, -1.0, 1.0]), static=True)


def log_background(
    stream: rr.RecordingStream, animation: Animation, *, patterns: Patterns
) -> None:
    for order, rendering in enumerate(animation.background):
        log_rendering(
            stream, rendering, draw_order=float(order), patterns=patterns, static=True
        )


def log_frames(
    stream: rr.RecordingStream,
    animation: Animation,
    *,
    timeline: Timeline,
    patterns: Patterns,
) -> None:
    for step, frame in enumerate(animation.frames):
        timeline.set_step(stream, step=step)
        for order, rendering in enumerate(frame.renderings):
            log_rendering(
                stream,
                rendering,
                draw_order=FRAME_DRAW_ORDER_OFFSET + order,
                patterns=patterns,
                static=False,
            )


def log_rendering(
    stream: rr.RecordingStream,
    rendering: Rendering,
    *,
    draw_order: float,
    patterns: Patterns,
    static: bool,
) -> None:
    stream.log(
        entities.rendering(rendering.name),
        archetype_of(rendering, draw_order=draw_order, patterns=patterns),
        static=static,
    )


def archetype_of(
    rendering: Rendering, *, draw_order: float, patterns: Patterns
) -> rr.LineStrips2D | rr.Points2D:
    match rendering:
        case Lines():
            return rr.LineStrips2D(
                patterns.strips(rendering),
                radii=radius_of(rendering.style.width),
                colors=tuple(rendering.style.color),
                draw_order=draw_order,
            )
        case Dots():
            return rr.Points2D(
                rendering.positions,
                radii=radius_of(rendering.style.size),
                colors=tuple(rendering.style.color),
                draw_order=draw_order,
            )


def radius_of(width: float) -> npt.ArrayLike:
    return rr.Radius.ui_points(width / 2)
