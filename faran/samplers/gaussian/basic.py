from typing import Final
from dataclasses import dataclass

from faran.types import (
    Array,
    NumPyControlInputBatchCreator,
    NumPyControlInputSequence,
    NumPyControlInputBatch,
    NumPySampler,
)
from faran.samplers.basic import StandardDeviationDescription, standardize

from jaxtyping import Float

import numpy as np


@dataclass(frozen=True)
class NumPyGaussianSampler[
    BatchT: NumPyControlInputBatch,
](NumPySampler[NumPyControlInputSequence, BatchT]):
    """Perturbs a nominal control sequence with zero-mean Gaussian noise."""

    standard_deviation: Final[Float[Array, " D_u"]]
    to_batch: Final[NumPyControlInputBatchCreator[BatchT]]
    rng: np.random.Generator

    _rollout_count: Final[int]

    @staticmethod
    def create[B: NumPyControlInputBatch](
        *,
        standard_deviation: StandardDeviationDescription,
        rollout_count: int,
        to_batch: NumPyControlInputBatchCreator,
        seed: int,
    ) -> "NumPyGaussianSampler":
        """Creates a sampler generating Gaussian noise around the specified control input
        sequence.

        Args:
            standard_deviation: Standard deviation of the perturbations, as one
                value for all control dimensions or one value per dimension.
            rollout_count: Number of rollouts M.
            to_batch: Wraps the sampled array in a control input batch.
            seed: Seed of the random number generator.
        """
        return NumPyGaussianSampler(
            standard_deviation=standardize.std(standard_deviation),
            to_batch=to_batch,
            rng=np.random.default_rng(seed),
            _rollout_count=rollout_count,
        )

    def sample(self, *, around: NumPyControlInputSequence) -> BatchT:
        samples = around.array[..., None] + self.rng.normal(
            loc=0.0,
            scale=self.standard_deviation[None, :, None],
            size=(around.horizon, around.dimension, self.rollout_count),
        )

        return self.to_batch(array=samples)

    @property
    def rollout_count(self) -> int:
        return self._rollout_count
