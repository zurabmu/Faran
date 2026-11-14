from typing import Final

from faran.collectors.registry import CollectorRegistry
from faran.collectors.obstacles import (
    ObstacleStateCollector,
    ObstacleObservationCollector,
    ObstacleForecastCollector,
)
from faran.collectors.risk import RiskCollector
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
    """Factory namespace for creating simulation data collectors."""

    class numpy:
        states: Final = StateCollector
        controls: Final = ControlCollector
        trajectories: Final = TrajectoryCollector
        risk: Final = RiskCollector
        obstacle_states: Final = ObstacleStateCollector
        obstacle_observations: Final = ObstacleObservationCollector
        obstacle_forecasts: Final = ObstacleForecastCollector
        registry: Final = CollectorRegistry.of

    class jax:
        states: Final = StateCollector
        controls: Final = ControlCollector
        trajectories: Final = TrajectoryCollector
        risk: Final = JaxRiskCollector
        obstacle_states: Final = ObstacleStateCollector
        obstacle_observations: Final = ObstacleObservationCollector
        obstacle_forecasts: Final = JaxObstacleForecastCollector
        registry: Final = CollectorRegistry.of
