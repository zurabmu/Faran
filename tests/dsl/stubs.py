from typing import Protocol, NamedTuple, Sequence, Any, Callable
from dataclasses import dataclass

from faran import (
    record,
    State,
    StateSequence,
    StateBatch,
    ControlInputBatch,
    ControlInputSequence,
    Distance,
    ObstacleIds,
    ObstacleStatesHistory,
    ObstacleStates,
    ObstacleStatesForTimeStep,
    SampledObstacleStates,
    BoundaryDistance,
    Control,
    DebugData,
    Costs,
    CostFunction as CostFunctionLike,
    Sampler as SamplerLike,
    ObstacleMotionPredictor as ObstacleMotionPredictorLike,
    ObstacleStateProvider as ObstacleStateProviderLike,
    ObstacleStateSampler as ObstacleStateSamplerLike,
    UpdateFunction as UpdateFunctionLike,
    PaddingFunction as PaddingFunctionLike,
    FilterFunction as FilterFunctionLike,
    DynamicalModel as DynamicalModelLike,
    DistanceExtractor as DistanceExtractorLike,
    BoundaryDistanceExtractor as BoundaryDistanceExtractorLike,
    Mppi as MppiLike,
    RiskMetric as RiskMetricLike,
    ObstacleStateObserver as ObstacleStateObserverLike,
)

import numpy as np


@dataclass(frozen=True, eq=False)
class Expectation:
    holds: Callable[[Any, Any], bool]
    message: str

    def receive(self, values: tuple[Any, Any], /) -> None:
        expected, actual = values
        assert self.holds(expected, actual), (
            f"{self.message} Expected: {expected}, Got: {actual}"
        )


class check:
    """Assertions that can be executed in compiled components (e.g. JAX JIT compiled functions)."""

    @staticmethod
    def equal(*, expected: Any, actual: Any, message: str) -> None:
        check.that(np.array_equal, expected=expected, actual=actual, message=message)

    @staticmethod
    def close(*, expected: Any, actual: Any, message: str) -> None:
        check.that(
            lambda expected, actual: np.allclose(expected, actual, atol=1e-6),
            expected=expected,
            actual=actual,
            message=message,
        )

    @staticmethod
    def that(
        holds: Callable[[Any, Any], bool], *, expected: Any, actual: Any, message: str
    ) -> None:
        record(Expectation(holds, message), (expected.array, actual.array))


@dataclass(frozen=True)
class Sampler[SequenceT: ControlInputSequence, BatchT: ControlInputBatch](
    SamplerLike[SequenceT, BatchT]
):
    samples: BatchT
    expected_nominal_input: SequenceT

    @staticmethod
    def returns[S: ControlInputSequence, B: ControlInputBatch](
        sampled_inputs: B, *, when_nominal_input_is: S
    ) -> "Sampler[S, B]":
        return Sampler(
            samples=sampled_inputs, expected_nominal_input=when_nominal_input_is
        )

    def sample(self, *, around: SequenceT) -> BatchT:
        check.equal(
            expected=self.expected_nominal_input,
            actual=around,
            message="Sampler received an unexpected nominal input.",
        )
        return self.samples

    @property
    def rollout_count(self) -> int:
        return self.samples.rollout_count


@dataclass(frozen=True)
class UpdateFunction[SequenceT: ControlInputSequence](UpdateFunctionLike[SequenceT]):
    expected_nominal_input: SequenceT
    expected_optimal_input: SequenceT
    result: SequenceT

    @staticmethod
    def returns[S: ControlInputSequence](
        result: S,
        *,
        when_nominal_input_is: S,
        and_optimal_input_is: S,
    ) -> "UpdateFunction[S]":
        return UpdateFunction(
            expected_nominal_input=when_nominal_input_is,
            expected_optimal_input=and_optimal_input_is,
            result=result,
        )

    def __call__(
        self, *, nominal_input: SequenceT, optimal_input: SequenceT
    ) -> SequenceT:
        check.equal(
            expected=self.expected_nominal_input,
            actual=nominal_input,
            message="UpdateFunction received an unexpected nominal input.",
        )
        check.close(
            expected=self.expected_optimal_input,
            actual=optimal_input,
            message="UpdateFunction received an unexpected optimal input.",
        )
        return self.result


@dataclass(frozen=True)
class PaddingFunction[NominalT: ControlInputSequence, PaddingT: ControlInputSequence](
    PaddingFunctionLike[NominalT, PaddingT]
):
    expected_nominal_input: NominalT
    expected_padding_size: int
    result: PaddingT

    @staticmethod
    def returns[N: ControlInputSequence, P: ControlInputSequence](
        result: P,
        *,
        when_nominal_input_is: N,
        and_padding_size_is: int,
    ) -> "PaddingFunction[N, P]":
        return PaddingFunction(
            expected_nominal_input=when_nominal_input_is,
            expected_padding_size=and_padding_size_is,
            result=result,
        )

    def __call__(self, *, nominal_input: NominalT, padding_size: int) -> PaddingT:
        check.equal(
            expected=self.expected_nominal_input,
            actual=nominal_input,
            message="PaddingFunction received an unexpected nominal input.",
        )
        assert self.expected_padding_size == padding_size, (
            f"PaddingFunction received an unexpected padding size. "
            f"Expected: {self.expected_padding_size}, Got: {padding_size}"
        )
        return self.result


@dataclass(frozen=True)
class FilterFunction[SequenceT: ControlInputSequence](FilterFunctionLike[SequenceT]):
    expected_optimal_input: SequenceT
    result: SequenceT

    @staticmethod
    def returns[S: ControlInputSequence](
        result: S,
        *,
        when_optimal_input_is: S,
    ) -> "FilterFunction[S]":
        return FilterFunction(
            expected_optimal_input=when_optimal_input_is,
            result=result,
        )

    def __call__(self, *, optimal_input: SequenceT) -> SequenceT:
        check.close(
            expected=self.expected_optimal_input,
            actual=optimal_input,
            message="FilterFunction received an unexpected optimal input.",
        )
        return self.result


@dataclass(frozen=True)
class DynamicalModel[
    StateT: State,
    StateSequenceT: StateSequence,
    StateBatchT: StateBatch,
    ControlInputSequenceT: ControlInputSequence,
    ControlInputBatchT: ControlInputBatch,
](
    DynamicalModelLike[
        StateT, StateSequenceT, StateBatchT, ControlInputSequenceT, ControlInputBatchT
    ]
):
    rollouts: StateBatchT
    expected_control_inputs: ControlInputBatchT
    expected_initial_state: StateT

    @staticmethod
    def returns[S: State, SB: StateBatch, CIB: ControlInputBatch](
        rollouts: SB, *, when_control_inputs_are: CIB, and_initial_state_is: S
    ) -> "DynamicalModel[S, StateSequence, SB, ControlInputSequence, CIB]":
        return DynamicalModel(
            rollouts=rollouts,
            expected_control_inputs=when_control_inputs_are,
            expected_initial_state=and_initial_state_is,
        )

    def simulate(
        self, inputs: ControlInputBatchT, initial_state: StateT
    ) -> StateBatchT:
        check.equal(
            expected=self.expected_control_inputs,
            actual=inputs,
            message="Dynamical model received unexpected control inputs.",
        )
        check.equal(
            expected=self.expected_initial_state,
            actual=initial_state,
            message="Dynamical model received an unexpected initial state.",
        )
        return self.rollouts

    def step(self, inputs: ControlInputSequenceT, state: StateT) -> StateT:
        raise NotImplementedError("Step method is not implemented in the stub model.")

    def forward(self, inputs: ControlInputSequenceT, state: StateT) -> StateSequenceT:
        raise NotImplementedError(
            "Forward method is not implemented in the stub model."
        )

    @property
    def time_step_size(self) -> float:
        raise NotImplementedError(
            "Time step size property is not implemented in the stub model."
        )


@dataclass(frozen=True)
class DistanceExtractor[
    StateT: StateBatch,
    SampleT: SampledObstacleStates,
    DistanceT: Distance,
](DistanceExtractorLike[StateT, SampleT, DistanceT]):
    expected_states: list[StateT]
    expected_obstacle_states: list[SampleT]
    result: list[DistanceT]

    @staticmethod
    def returns[SB: StateBatch, SOS: SampledObstacleStates, D: Distance](
        distances: D,
        *,
        when_states_are: SB,
        and_obstacle_states_are: SOS,
    ) -> "DistanceExtractor[SB, SOS, D]":
        return DistanceExtractor(
            expected_states=[when_states_are],
            expected_obstacle_states=[and_obstacle_states_are],
            result=[distances],
        )

    def __call__(self, *, states: StateT, obstacle_states: SampleT) -> DistanceT:
        for expected_states, expected_obstacle_states, result in self.result_variants:
            if np.array_equal(expected_states, states) and np.array_equal(
                expected_obstacle_states, obstacle_states
            ):
                return result

        assert False, (
            f"DistanceExtractor received unexpected inputs. "
            f"States: {states}, Obstacle States: {obstacle_states}"
        )

    def or_returns(
        self,
        distances: DistanceT,
        *,
        when_states_are: StateT,
        and_obstacle_states_are: SampleT,
    ) -> "DistanceExtractor[StateT, SampleT, DistanceT]":
        self.expected_states.append(when_states_are)
        self.expected_obstacle_states.append(and_obstacle_states_are)
        self.result.append(distances)

        return self

    @property
    def result_variants(self) -> Sequence[tuple[StateT, SampleT, DistanceT]]:
        return list(
            zip(self.expected_states, self.expected_obstacle_states, self.result)
        )


@dataclass(frozen=True)
class ObstacleMotionPredictor[
    HistoryT: ObstacleStatesHistory,
    PredictionT: ObstacleStates,
](ObstacleMotionPredictorLike[HistoryT, PredictionT]):
    expected_history: HistoryT
    result: PredictionT

    @staticmethod
    def returns[H: ObstacleStatesHistory, P: ObstacleStates](
        result: P, *, when_history_is: H
    ) -> "ObstacleMotionPredictor[H, P]":
        return ObstacleMotionPredictor(
            expected_history=when_history_is,
            result=result,
        )

    def predict(self, *, history: HistoryT) -> PredictionT:
        assert np.array_equal(self.expected_history, history, equal_nan=True), (
            f"ObstacleMotionPredictor received unexpected history. "
            f"Expected: {self.expected_history}, Got: {history}"
        )
        return self.result


@dataclass(frozen=True)
class EchoingObstacleMotionPredictor[StatesT: ObstacleStates](
    ObstacleMotionPredictorLike[StatesT, StatesT]
):
    """Returns the history as the prediction."""

    @staticmethod
    def create[S: ObstacleStates]() -> "EchoingObstacleMotionPredictor[S]":
        return EchoingObstacleMotionPredictor()

    def predict(self, *, history: StatesT) -> StatesT:
        return history


@dataclass(frozen=True)
class ObstacleIdAssignment[
    IdT: ObstacleIds,
    ObservationT: ObstacleStatesForTimeStep,
    HistoryT: ObstacleStatesHistory,
]:
    class Entry[I, O, H](NamedTuple):
        ids: I
        when_observing: O
        and_history: H | None = None
        and_ids: I | None = None

    class Provider[I, O, H](Protocol):
        def __call__(
            self,
            ids: type["ObstacleIdAssignment.Entry[I, O, H]"],
            /,
        ) -> Sequence["ObstacleIdAssignment.Entry[I, O, H]"]:
            """Describes how obstacle IDs are assigned based on observations."""
            ...

    assignments: Sequence[Entry[IdT, ObservationT, HistoryT]]

    @staticmethod
    def returns[I: ObstacleIds, O: ObstacleStatesForTimeStep, H: ObstacleStatesHistory](
        provider: "ObstacleIdAssignment.Provider[I, O, H]",
    ) -> "ObstacleIdAssignment[I, O, H]":
        return ObstacleIdAssignment(assignments=provider(ObstacleIdAssignment.Entry))

    def __call__(
        self, states: ObservationT, /, *, history: HistoryT, ids: IdT
    ) -> IdT | None:
        for entry in self.assignments:
            if np.array_equal(entry.when_observing, states):
                assert entry.and_history is None or np.array_equal(
                    entry.and_history, history, equal_nan=True
                ), (
                    f"Received unexpected history for ID assignment. "
                    f"Expected: {entry.and_history}, Got: {history}"
                )
                assert entry.and_ids is None or np.array_equal(entry.and_ids, ids), (
                    f"Received unexpected IDs for ID assignment. "
                    f"Expected: {entry.and_ids}, Got: {ids}"
                )

                return entry.ids

        assert False, f"Could not find ID assignment for the observation: {states}"


@dataclass(frozen=True)
class ObstacleStateProvider[ObstacleStatesT: ObstacleStates](
    ObstacleStateProviderLike[ObstacleStatesT]
):
    result: ObstacleStatesT

    @staticmethod
    def returns[O: ObstacleStates](result: O) -> "ObstacleStateProvider[O]":
        return ObstacleStateProvider(result=result)

    def __call__(self) -> ObstacleStatesT:
        return self.result


@dataclass(frozen=True)
class ObstacleStateSampler[StateT: ObstacleStates, SampleT: SampledObstacleStates](
    ObstacleStateSamplerLike[StateT, SampleT]
):
    expected_obstacle_states: StateT
    expected_sample_count: int
    result: SampleT

    @staticmethod
    def returns[O: ObstacleStates, S: SampledObstacleStates](
        result: S,
        *,
        when_obstacle_states_are: O,
        and_sample_count_is: int,
    ) -> "ObstacleStateSampler[O, S]":
        return ObstacleStateSampler(
            expected_obstacle_states=when_obstacle_states_are,
            expected_sample_count=and_sample_count_is,
            result=result,
        )

    def __call__(self, states: StateT, *, count: int) -> SampleT:
        assert np.array_equal(self.expected_obstacle_states, states), (
            f"ObstacleStateSampler received unexpected obstacle states. "
            f"Expected: {self.expected_obstacle_states}, Got: {states}"
        )
        assert self.expected_sample_count == count, (
            f"ObstacleStateSampler received an unexpected sample count. "
            f"Expected: {self.expected_sample_count}, Got: {count}"
        )
        return self.result


@dataclass(frozen=True)
class BoundaryDistanceExtractor[StateT: StateBatch, DistanceT: BoundaryDistance](
    BoundaryDistanceExtractorLike[StateT, DistanceT]
):
    expected_states: StateT
    result: DistanceT

    @staticmethod
    def returns[SB: StateBatch, BD: BoundaryDistance](
        distances: BD, *, when_states_are: SB
    ) -> "BoundaryDistanceExtractor[SB, BD]":
        return BoundaryDistanceExtractor(
            expected_states=when_states_are, result=distances
        )

    def __call__(self, *, states: StateT) -> DistanceT:
        assert np.array_equal(self.expected_states, states), (
            f"BoundaryDistanceExtractor received unexpected states. "
            f"Expected: {self.expected_states}, Got: {states}"
        )
        return self.result


@dataclass(frozen=True)
class RiskMetric[RiskT](RiskMetricLike[Any, Any, Any, Any, RiskT]):
    result: RiskT

    @staticmethod
    def returns[R](result: R) -> "RiskMetric[R]":
        return RiskMetric(result=result)

    def compute(
        self,
        cost_function: Any,
        *,
        states: Any,
        obstacle_states: Any,
        sampler: Any,
    ) -> RiskT:
        return self.result

    @property
    def name(self) -> str:
        return "Stub"


@dataclass(frozen=True)
class RiskComputingCostFunction[
    InputBatchT: ControlInputBatch,
    StateBatchT: StateBatch,
    CostsT: Costs,
](CostFunctionLike[InputBatchT, StateBatchT, CostsT]):
    inner: CostFunctionLike[InputBatchT, StateBatchT, CostsT]
    risk_metric: RiskMetricLike[Any, StateBatchT, None, None, Any]

    @staticmethod
    def wrapping[IB: ControlInputBatch, SB: StateBatch, C: Costs](
        inner: CostFunctionLike[IB, SB, C],
        *,
        computing_risk_with: RiskMetricLike[Any, SB, None, None, Any],
    ) -> "RiskComputingCostFunction[IB, SB, C]":
        return RiskComputingCostFunction(inner=inner, risk_metric=computing_risk_with)

    def __call__(self, *, inputs: InputBatchT, states: StateBatchT) -> CostsT:
        self.risk_metric.compute(
            self.inner, states=states, obstacle_states=None, sampler=None
        )
        return self.inner(inputs=inputs, states=states)


@dataclass(frozen=True)
class ObstacleStatesReadingCostFunction[
    InputBatchT: ControlInputBatch,
    StateBatchT: StateBatch,
    CostsT: Costs,
](CostFunctionLike[InputBatchT, StateBatchT, CostsT]):
    inner: CostFunctionLike[InputBatchT, StateBatchT, CostsT]
    obstacle_states: ObstacleStateProviderLike[Any]

    @staticmethod
    def wrapping[IB: ControlInputBatch, SB: StateBatch, C: Costs](
        inner: CostFunctionLike[IB, SB, C],
        *,
        reading_obstacle_states_from: ObstacleStateProviderLike[Any],
    ) -> "ObstacleStatesReadingCostFunction[IB, SB, C]":
        return ObstacleStatesReadingCostFunction(
            inner=inner, obstacle_states=reading_obstacle_states_from
        )

    def __call__(self, *, inputs: InputBatchT, states: StateBatchT) -> CostsT:
        self.obstacle_states()
        return self.inner(inputs=inputs, states=states)


@dataclass(frozen=True)
class Mppi(MppiLike):
    @staticmethod
    def create() -> "Mppi":
        return Mppi()

    def step(
        self,
        *,
        temperature: float,
        nominal_input: Any,
        initial_state: Any,
    ) -> Control[Any, Any]:
        return Control(
            optimal=nominal_input,
            nominal=nominal_input,
            debug=DebugData(trajectory_weights=None),
        )


@dataclass(frozen=True)
class ObstacleStateObserver[ObstacleStatesForTimeStepT](
    ObstacleStateObserverLike[ObstacleStatesForTimeStepT]
):
    @staticmethod
    def create() -> "ObstacleStateObserver[ObstacleStatesForTimeStepT]":
        return ObstacleStateObserver()

    def observe(self, states: ObstacleStatesForTimeStepT) -> None: ...


class NoiseModel[NoiseT](NamedTuple):
    noise: NoiseT

    def __call__(
        self, *, noise: NoiseT, prediction: Any, observation: Any, state: None
    ) -> tuple[NoiseT, None]:
        return self.noise, None

    @property
    def state(self) -> None:
        return None


class NoiseModelProvider[NoiseT](NamedTuple):
    noise: NoiseT

    @staticmethod
    def returning[N](noise: N) -> "NoiseModelProvider[N]":
        return NoiseModelProvider(noise)

    def __call__(
        self, *, obstacle_count: int, observation_matrix: Any, noise: NoiseT
    ) -> NoiseModel[NoiseT]:
        return NoiseModel(noise)
