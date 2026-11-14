from dataclasses import dataclass, field

from faran.types import Risk, RiskMetric, ObstacleStateProvider, pytree, record
from faran.collectors.access import access
from faran.collectors.registry import (
    DataTransformer,
    IdentityTransformer,
    ModificationNotifierMixin,
    ListCollectorMixin,
    OnModifyCallback,
)


@dataclass(frozen=True)
class JaxRiskCollector[
    CostFunctionT,
    StateBatchT,
    ObstacleStatesT,
    SamplerT,
    RiskT = Risk,
](
    RiskMetric[CostFunctionT, StateBatchT, ObstacleStatesT, SamplerT, RiskT],
    ModificationNotifierMixin,
    ListCollectorMixin,
):
    """Decorator collecting computed risk values at each evaluation. Works inside JIT compiled functions."""

    inner: RiskMetric[CostFunctionT, StateBatchT, ObstacleStatesT, SamplerT, RiskT]
    transformer: DataTransformer[RiskT]
    _callbacks: list[OnModifyCallback] = field(default_factory=list)
    _collected: list[RiskT] = pytree.static_field(default_factory=list)

    @staticmethod
    def decorating[CF, SB, OS, S, R](
        metric: RiskMetric[CF, SB, OS, S, R],
        *,
        transformer: DataTransformer[R] = IdentityTransformer(),
    ) -> "JaxRiskCollector[CF, SB, OS, S, R]":
        return JaxRiskCollector(metric, transformer=transformer)

    def compute(
        self,
        cost_function: CostFunctionT,
        *,
        states: StateBatchT,
        obstacle_states: ObstacleStatesT,
        sampler: SamplerT,
    ) -> RiskT:
        risk = self.inner.compute(
            cost_function,
            states=states,
            obstacle_states=obstacle_states,
            sampler=sampler,
        )
        record(self, risk)
        return risk

    def receive(self, risk: RiskT, /) -> None:
        self._collected.append(risk)
        self.notify()

    @property
    def name(self) -> str:
        return self.inner.name

    @property
    def key(self) -> str:
        return access.risks.key


@dataclass(frozen=True)
class JaxObstacleForecastCollector[ObstacleStatesT](
    ObstacleStateProvider[ObstacleStatesT],
    ModificationNotifierMixin,
    ListCollectorMixin,
):
    """Decorator collecting predicted obstacle state forecasts. Works inside JIT compiled functions."""

    inner: ObstacleStateProvider[ObstacleStatesT]
    transformer: DataTransformer[ObstacleStatesT]
    _callbacks: list[OnModifyCallback] = field(default_factory=list)
    _collected: list[ObstacleStatesT] = pytree.static_field(default_factory=list)

    @staticmethod
    def decorating[OS](
        provider: ObstacleStateProvider[OS],
        *,
        transformer: DataTransformer[OS] = IdentityTransformer(),
    ) -> "JaxObstacleForecastCollector[OS]":
        return JaxObstacleForecastCollector(provider, transformer=transformer)

    def __call__(self) -> ObstacleStatesT:
        states = self.inner()
        record(self, states)
        return states

    def receive(self, states: ObstacleStatesT, /) -> None:
        self._collected.append(states)
        self.notify()

    @property
    def key(self) -> str:
        return access.obstacle_forecasts.key
