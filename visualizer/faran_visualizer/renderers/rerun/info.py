from typing import Sequence

from faran_visualizer.renderers.rerun.entities import entities
from faran_visualizer.renderers.rerun.timeline import Timeline
from faran_visualizer.scene import Row, Animation

import rerun as rr


def log_info(
    stream: rr.RecordingStream, animation: Animation, *, timeline: Timeline
) -> None:
    for step, frame in enumerate(animation.frames):
        timeline.set_step(stream, step=step)
        stream.log(
            entities.info,
            rr.TextDocument(
                markdown_table(frame.info), media_type=rr.MediaType.MARKDOWN
            ),
        )


def markdown_table(rows: Sequence[Row]) -> str:
    return "\n".join(
        ["| | |", "|---|---|", *(f"| {row.label} | {text_of(row)} |" for row in rows)]
    )


def text_of(row: Row) -> str:
    value = f"{row.value:.2f}"
    return value if row.unit is None else f"{value} {row.unit}"
