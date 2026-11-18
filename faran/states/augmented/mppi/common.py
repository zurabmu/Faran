from typing import Protocol, NamedTuple

from faran.types import (
    Mppi,
    DynamicalModel,
    Sampler,
    CostFunction,
    AugmentedState,
    AugmentedStateSequence,
    AugmentedStateBatch,
    AugmentedControlInputSequence,
    AugmentedControlInputBatch,
    AugmentedStateCreator,
    AugmentedStateSequenceCreator,
    AugmentedStateBatchCreator,
    AugmentedControlInputBatchCreator,
)
from faran.states.augmented.common import AugmentedModel, AugmentedSampler


class MppiCreator[
    StateT,
    StateSequenceT,
    StateBatchT,
    InputSequenceT,
    WeightsT,
    InputBatchT,
    CostsT,
](Protocol):
    """Protocol for callables that create an MPPI planner from model, sampler, and cost."""

    def __call__(
        self,
        model: DynamicalModel[
            StateT, StateSequenceT, StateBatchT, InputSequenceT, InputBatchT
        ],
        sampler: Sampler[InputSequenceT, InputBatchT],
        cost: CostFunction[InputBatchT, StateBatchT, CostsT],
    ) -> Mppi[StateT, InputSequenceT, WeightsT]:
        """Creates an MPPI planner from the specified components."""
        ...


class AugmentedMppiSetup[MppiT, ModelT](NamedTuple):
    """Bundled result of augmented MPPI creation containing the planner and its model."""

    mppi: MppiT
    model: ModelT


class AugmentedMppi:
    """Generic factory for MPPI planners with augmented (physical + virtual) state spaces."""

    @staticmethod
    def create[
        PS,
        PSS,
        PSB,
        PIS,
        PIB,
        VS,
        VSS,
        VSB,
        VIS,
        VIB,
        AS: AugmentedState,
        ASS: AugmentedStateSequence,
        ASB: AugmentedStateBatch,
        AIS: AugmentedControlInputSequence,
        AIB: AugmentedControlInputBatch,
        W,
        C,
    ](
        *,
        mppi: MppiCreator[AS, ASS, ASB, AIS, W, AIB, C],
        models: tuple[
            DynamicalModel[PS, PSS, PSB, PIS, PIB],
            DynamicalModel[VS, VSS, VSB, VIS, VIB],
        ],
        samplers: tuple[Sampler[PIS, PIB], Sampler[VIS, VIB]],
        cost: CostFunction[AIB, ASB, C],
        state: AugmentedStateCreator[PS, VS, AS],
        state_sequence: AugmentedStateSequenceCreator[PSS, VSS, ASS],
        state_batch: AugmentedStateBatchCreator[PSB, VSB, ASB],
        input_batch: AugmentedControlInputBatchCreator[PIB, VIB, AIB],
    ) -> AugmentedMppiSetup[
        Mppi[AS, AIS, W],
        AugmentedModel[PS, PSS, PSB, PIS, PIB, VS, VSS, VSB, VIS, VIB, AS, ASS, ASB],
    ]:
        return AugmentedMppiSetup(
            mppi=mppi(
                model=(
                    model := AugmentedModel.of(
                        physical=models[0],
                        virtual=models[1],
                        state=state,
                        sequence=state_sequence,
                        batch=state_batch,
                    )
                ),
                sampler=AugmentedSampler.of(
                    physical=samplers[0], virtual=samplers[1], batch=input_batch
                ),
                cost=cost,
            ),
            model=model,
        )
