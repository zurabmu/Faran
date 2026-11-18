from typing import Final

from faran.trajectories.line import JaxLineTrajectory
from faran.trajectories.waypoints import (
    JaxWaypointsTrajectory,
)


class trajectory:
    line: Final = JaxLineTrajectory.create
    waypoints: Final = JaxWaypointsTrajectory.create
