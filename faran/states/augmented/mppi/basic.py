from faran.types import (
    Mppi,
    NumPyState,
    NumPyStateSequence,
    NumPyStateBatch,
    NumPyControlInputSequence,
    NumPyControlInputBatch,
    NumPyDynamicalModel,
    NumPyCosts,
    NumPyCostFunction,
    NumPySampler,
    NumPyUpdateFunction,
    NumPyPaddingFunction,
    NumPyFilterFunction,
    AugmentedStateCreator,
    AugmentedStateSequenceCreator,
    AugmentedStateBatchCreator,
    AugmentedControlInputBatchCreator,
)
from faran.mppi import NumPyWeights, NumPyMppi
from faran.states.augmented.basic import (
    NumPyAugmentedState,
    NumPyAugmentedStateSequence,
    NumPyAugmentedStateBatch,
    NumPyAugmentedControlInputSequence,
    NumPyAugmentedControlInputBatch,
)
from faran.states.augmented.common import AugmentedModel
from faran.states.augmented.mppi.common import AugmentedMppi, AugmentedMppiSetup


class NumPyAugmentedMppi:
    """Factory for NumPy MPPI planners with augmented state spaces."""

    @staticmethod
    def create[
        PS: NumPyState,
        PSS: NumPyStateSequence,
        PSB: NumPyStateBatch,
        PCS: NumPyControlInputSequence,
        PCB: NumPyControlInputBatch,
        VS: NumPyState,
        VSS: NumPyStateSequence,
        VSB: NumPyStateBatch,
        VCS: NumPyControlInputSequence,
        VCB: NumPyControlInputBatch,
        AS: NumPyAugmentedState,
        ASS: NumPyAugmentedStateSequence,
        ASB: NumPyAugmentedStateBatch,
        ACS: NumPyAugmentedControlInputSequence,
        C: NumPyCosts,
    ](
        *,
        planning_interval: int = 1,
        models: tuple[
            NumPyDynamicalModel[PS, PSS, PSB, PCS, PCB],
            NumPyDynamicalModel[VS, VSS, VSB, VCS, VCB],
        ],
        samplers: tuple[NumPySampler[PCS, PCB], NumPySampler[VCS, VCB]],
        cost: NumPyCostFunction,
        state: AugmentedStateCreator[PS, VS, AS],
        state_sequence: AugmentedStateSequenceCreator[PSS, VSS, ASS],
        state_batch: AugmentedStateBatchCreator[PSB, VSB, ASB],
        input_batch: AugmentedControlInputBatchCreator[
            PCB, VCB, NumPyAugmentedControlInputBatch[PCB, VCB]
        ],
        update_function: NumPyUpdateFunction[ACS] | None = None,
        padding_function: NumPyPaddingFunction[ACS, NumPyAugmentedControlInputSequence]
        | None = None,
        filter_function: NumPyFilterFunction[ACS] | None = None,
    ) -> AugmentedMppiSetup[
        Mppi[AS, ACS, NumPyWeights],
        AugmentedModel[PS, PSS, PSB, PCS, PCB, VS, VSS, VSB, VCS, VCB, AS, ASS, ASB],
    ]:
        return AugmentedMppi.create(
            mppi=lambda model, sampler, cost: NumPyMppi.create(
                planning_interval=planning_interval,
                model=model,
                cost_function=cost,
                sampler=sampler,
                update_function=update_function,
                padding_function=padding_function,
                filter_function=filter_function,
            ),
            models=models,
            samplers=samplers,
            cost=cost,
            state=state,
            state_sequence=state_sequence,
            state_batch=state_batch,
            input_batch=input_batch,
        )
