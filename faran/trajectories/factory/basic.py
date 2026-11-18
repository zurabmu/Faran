from typing import Final

from faran.trajectories.line import NumPyLineTrajectory
from faran.trajectories.waypoints import (
    NumPyWaypointsTrajectory,
)


class trajectory:
    line: Final = NumPyLineTrajectory.create
    waypoints: Final = NumPyWaypointsTrajectory.create
