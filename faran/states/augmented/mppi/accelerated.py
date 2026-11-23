from faran.types import (
    Mppi,
    JaxState,
    JaxStateSequence,
    JaxStateBatch,
    JaxControlInputSequence,
    JaxControlInputBatch,
    JaxDynamicalModel,
    JaxCosts,
    JaxCostFunction,
    JaxSampler,
    JaxUpdateFunction,
    JaxPaddingFunction,
    JaxFilterFunction,
    AugmentedStateCreator,
    AugmentedStateSequenceCreator,
    AugmentedStateBatchCreator,
    AugmentedControlInputBatchCreator,
)
from faran.mppi import JaxWeights, JaxMppi
from faran.states.augmented.accelerated import (
    JaxAugmentedState,
    JaxAugmentedStateSequence,
    JaxAugmentedStateBatch,
    JaxAugmentedControlInputSequence,
    JaxAugmentedControlInputBatch,
)
from faran.states.augmented.common import AugmentedModel
from faran.states.augmented.mppi.common import AugmentedMppi, AugmentedMppiSetup


class JaxAugmentedMppi:
    """Factory for JAX MPPI planners with augmented state spaces."""

    @staticmethod
    def create[
        PS: JaxState,
        PSS: JaxStateSequence,
        PSB: JaxStateBatch,
        PCS: JaxControlInputSequence,
        PCB: JaxControlInputBatch,
        VS: JaxState,
        VSS: JaxStateSequence,
        VSB: JaxStateBatch,
        VCS: JaxControlInputSequence,
        VCB: JaxControlInputBatch,
        AS: JaxAugmentedState,
        ASS: JaxAugmentedStateSequence,
        ASB: JaxAugmentedStateBatch,
        ACS: JaxAugmentedControlInputSequence,
        C: JaxCosts,
    ](
        *,
        planning_interval: int = 1,
        models: tuple[
            JaxDynamicalModel[PS, PSS, PSB, PCS, PCB],
            JaxDynamicalModel[VS, VSS, VSB, VCS, VCB],
        ],
        samplers: tuple[JaxSampler[PCS, PCB], JaxSampler[VCS, VCB]],
        cost: JaxCostFunction,
        state: AugmentedStateCreator[PS, VS, AS],
        state_sequence: AugmentedStateSequenceCreator[PSS, VSS, ASS],
        state_batch: AugmentedStateBatchCreator[PSB, VSB, ASB],
        input_batch: AugmentedControlInputBatchCreator[
            PCB, VCB, JaxAugmentedControlInputBatch[PCB, VCB]
        ],
        update_function: JaxUpdateFunction[ACS] | None = None,
        padding_function: JaxPaddingFunction[ACS, JaxAugmentedControlInputSequence]
        | None = None,
        filter_function: JaxFilterFunction[ACS] | None = None,
    ) -> AugmentedMppiSetup[
        Mppi[AS, ACS, JaxWeights],
        AugmentedModel[PS, PSS, PSB, PCS, PCB, VS, VSS, VSB, VCS, VCB, AS, ASS, ASB],
    ]:
        """Creates an MPPI planner whose state joins the states of a physical and a virtual
        model, for example the path parameter of MPCC.

        Args:
            models: The physical and the virtual dynamics model.
            samplers: Samplers for the physical and the virtual control inputs.
            cost: Scores each rollout of the augmented state.
            state: Creates an augmented state from a physical and a virtual state.
            state_sequence: Creates an augmented state sequence.
            state_batch: Creates an augmented state batch.
            input_batch: Creates an augmented control input batch.
            planning_interval: Number of time steps that the nominal sequence is
                shifted by after each planner step. Must be positive.
            update_function: Computes the next nominal sequence from the optimal
                one. Without one, the optimal sequence becomes the nominal sequence.
            padding_function: Fills the time steps at the end of the shifted nominal
                sequence. Without one, they are filled with zeros.
            filter_function: Smooths the optimal sequence, for example a
                Savitzky-Golay filter. Without one, it is not filtered.
        """
        return AugmentedMppi.create(
            mppi=lambda model, sampler, cost: JaxMppi.create(
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
