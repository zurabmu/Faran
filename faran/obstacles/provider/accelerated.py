from dataclasses import dataclass

from faran.types import (
    ObstacleStatesForTimeStep,
    ObstacleStateProvider,
    ObstacleMotionPredictor,
    ObstacleStatesRunningHistory,
    ObstacleIdAssignment,
    Variable,
    pytree,
)
from faran.obstacles.provider.common import DefaultIdAssignment


@dataclass
class CurrentHistory[ObstacleStatesForTimeStepT, IdT, HistoryT]:
    value: ObstacleStatesRunningHistory[ObstacleStatesForTimeStepT, IdT, HistoryT]


@dataclass(frozen=True, kw_only=True)
class JaxPredictingObstacleStateProvider[
    ObstacleStatesForTimeStepT,
    IdT,
    HistoryT,
    PredictionT,
](ObstacleStateProvider[PredictionT]):
    """Provides obstacle state predictions by maintaining a running history and forwarding to a
    predictor. Inside compiled planner steps, it predicts from the history as of the last
    observation.
    """

    predictor: ObstacleMotionPredictor[HistoryT, PredictionT]
    id_assignment: ObstacleIdAssignment[ObstacleStatesForTimeStepT, IdT, HistoryT]
    # NOTE: The running history is updated outside of compiled planner steps, so it is not
    # traced. The provider reads the states of the history from `states` instead.
    history: CurrentHistory[ObstacleStatesForTimeStepT, IdT, HistoryT] = (
        pytree.static_field()
    )
    states: Variable[HistoryT]

    @staticmethod
    def create[O: ObstacleStatesForTimeStep, I, H, P](
        *,
        predictor: ObstacleMotionPredictor[H, P],
        history: ObstacleStatesRunningHistory[O, I, H],
        id_assignment: ObstacleIdAssignment[O, I, H] | None = None,
    ) -> "JaxPredictingObstacleStateProvider[O, I, H, P]":
        return JaxPredictingObstacleStateProvider(
            predictor=predictor,
            id_assignment=id_assignment
            if id_assignment is not None
            else DefaultIdAssignment(),
            history=CurrentHistory(history),
            states=Variable.create(history.get()),
        )

    def __call__(self) -> PredictionT:
        return self.predictor.predict(history=self.states.get())

    def observe(self, states: ObstacleStatesForTimeStepT) -> None:
        history = self.history.value
        self.history.value = history.append(
            states,
            ids=self.id_assignment(states, history=history.get(), ids=history.ids()),
        )
        self.states.set(self.history.value.get())
