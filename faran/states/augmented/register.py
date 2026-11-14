from faran.states.augmented.base import (
    BaseAugmentedState,
    BaseAugmentedStateSequence,
    BaseAugmentedStateBatch,
    BaseAugmentedControlInputSequence,
    BaseAugmentedControlInputBatch,
)
from faran.types import pytree


def register_shared_types_as_pytrees() -> None:
    pytree(BaseAugmentedState)
    pytree(BaseAugmentedStateSequence)
    pytree(BaseAugmentedStateBatch)
    pytree(BaseAugmentedControlInputSequence)
    pytree(BaseAugmentedControlInputBatch)
