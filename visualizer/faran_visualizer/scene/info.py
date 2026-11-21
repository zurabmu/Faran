from typing import Sequence

from faran_visualizer.scene.description import Info
from faran_visualizer.scene.animation import Row


def rows_at(info: Sequence[Info], *, step: int) -> list[Row]:
    return [
        Row(label=it.label, value=float(it.values[step]), unit=it.unit) for it in info
    ]
