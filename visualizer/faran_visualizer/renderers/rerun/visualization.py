from typing import Final
from pathlib import Path

from faran_visualizer.renderers.rerun.charts import log_charts
from faran_visualizer.renderers.rerun.renderings import (
    Patterns,
    log_background,
    log_frames,
    log_scene_frame,
)
from faran_visualizer.renderers.rerun.info import log_info
from faran_visualizer.renderers.rerun.layout import blueprint_for
from faran_visualizer.renderers.rerun.timeline import Timeline
from faran_visualizer.scene import Animation

import rerun as rr

APPLICATION_ID: Final = "faran"


def save(animation: Animation, *, name: str, to: Path) -> None:
    """Saves the animation as a Rerun visualization. `name` is the visualization name that the
    viewer shows."""
    timeline = Timeline(step_count=len(animation.frames), time_step=animation.time_step)
    patterns = Patterns.for_animation(animation)
    stream = rr.RecordingStream(application_id=APPLICATION_ID)

    stream.save(to, default_blueprint=blueprint_for(animation, timeline=timeline))
    stream.send_recording_name(name)
    log_scene_frame(stream)
    log_background(stream, animation, patterns=patterns)
    log_frames(stream, animation, timeline=timeline, patterns=patterns)
    log_info(stream, animation, timeline=timeline)
    log_charts(stream, animation, timeline=timeline)
    stream.flush()
    stream.disconnect()
