from typing import Final, Sequence
from dataclasses import dataclass

import rerun as rr
import rerun.blueprint as rrb

STEP_TIMELINE: Final = "step"
TIME_TIMELINE: Final = "time"


@dataclass(kw_only=True, frozen=True)
class Timeline:
    step_count: int
    time_step: float

    @property
    def steps(self) -> range:
        return range(self.step_count)

    def set_step(self, stream: rr.RecordingStream, *, step: int) -> None:
        stream.set_time(STEP_TIMELINE, sequence=step)
        stream.set_time(TIME_TIMELINE, duration=step * self.time_step)

    def columns(self, steps: Sequence[int]) -> list[rr.TimeColumn]:
        return [
            rr.TimeColumn(STEP_TIMELINE, sequence=list(steps)),
            rr.TimeColumn(
                TIME_TIMELINE, duration=[step * self.time_step for step in steps]
            ),
        ]

    def time_panel(self) -> rrb.TimePanel:
        return rrb.TimePanel(timeline=TIME_TIMELINE)
