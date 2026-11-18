from typing import Final

from faran.collectors.registry import CollectorRegistry
from faran.collectors.obstacles import (
    ObstacleStateCollector,
    ObstacleObservationCollector,
)
from faran.collectors.state import (
    StateCollector,
    ControlCollector,
    TrajectoryCollector,
)
from faran.collectors.accelerated import (
    JaxRiskCollector,
    JaxObstacleForecastCollector,
)


class collectors:
    states: Final = StateCollector
    controls: Final = ControlCollector
    trajectories: Final = TrajectoryCollector
    risk: Final = JaxRiskCollector
    obstacle_states: Final = ObstacleStateCollector
    obstacle_observations: Final = ObstacleObservationCollector
    obstacle_forecasts: Final = JaxObstacleForecastCollector
    registry: Final = CollectorRegistry.of
