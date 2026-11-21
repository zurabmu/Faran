from faran_visualizer.array import Array
from faran_visualizer.scene import Info

from jaxtyping import Float

import numpy as np


def ego_info(
    *,
    time_step: float,
    x: Float[Array, " T"],
    y: Float[Array, " T"],
    heading: Float[Array, " T"],
    path_parameters: Float[Array, " T"],
    path_length: float,
) -> list[Info]:
    """Returns the time, position, heading and path progress of the ego."""
    return [
        Info(label="Time", values=np.arange(len(x)) * time_step, unit="s"),
        Info(label="X", values=x, unit="m"),
        Info(label="Y", values=y, unit="m"),
        Info(label="Heading", values=np.degrees(heading), unit="°"),
        Info(label="Path Parameter", values=path_parameters, unit="m"),
        Info(label="Progress", values=100 * path_parameters / path_length, unit="%"),
    ]
