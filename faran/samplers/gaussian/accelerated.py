from dataclasses import dataclass

from faran.types import (
    pytree,
    jaxtyped,
    JaxControlInputBatchCreator,
    JaxControlInputSequence,
    JaxControlInputBatch,
    JaxSampler,
)
from faran.samplers.accelerated import StandardDeviationDescription, standardize

from jaxtyping import Array as JaxArray, Float, PRNGKeyArray

import jax
import jax.random as jrandom


@dataclass(frozen=True, kw_only=True)
class JaxGaussianSampler[BatchT: JaxControlInputBatch](
    JaxSampler[JaxControlInputSequence, BatchT]
):
    """Perturbs a nominal control sequence with zero-mean Gaussian noise."""

    standard_deviation: Float[JaxArray, " D_u"]
    to_batch: JaxControlInputBatchCreator[BatchT]
    key: pytree.Variable[PRNGKeyArray]

    _rollout_count: int

    @staticmethod
    def create[B: JaxControlInputBatch](
        *,
        standard_deviation: StandardDeviationDescription,
        rollout_count: int,
        to_batch: JaxControlInputBatchCreator,
        key: PRNGKeyArray | None = None,
        seed: int | None = None,
    ) -> "JaxGaussianSampler":
        """Creates a sampler generating Gaussian noise around the specified control input
        sequence.

        Args:
            standard_deviation: Standard deviation of the perturbations, as one
                value for all control dimensions or one value per dimension.
            rollout_count: Number of rollouts M.
            to_batch: Wraps the sampled array in a control input batch.
            key: JAX random key. Takes precedence over `seed`.
            seed: Seed of the random key, used when `key` is not given.
        """
        return JaxGaussianSampler(
            standard_deviation=standardize.std(standard_deviation),
            to_batch=to_batch,
            _rollout_count=rollout_count,
            key=pytree.variable(key if key is not None else jrandom.key(seed or 0)),
        )

    def sample(self, *, around: JaxControlInputSequence) -> BatchT:
        key, samples = sample(
            self.key.get(),
            around=around.array,
            standard_deviation=self.standard_deviation,
            rollout_count=self.rollout_count,
        )
        self.key.set(key)

        return self.to_batch(array=samples)

    @property
    def rollout_count(self) -> int:
        return self._rollout_count


@jax.jit(static_argnames=("rollout_count",))
@jaxtyped
def sample(
    key: PRNGKeyArray,
    *,
    around: Float[JaxArray, "T D_u"],
    standard_deviation: Float[JaxArray, " D_u"],
    rollout_count: int,
) -> tuple[PRNGKeyArray, Float[JaxArray, "T D_u M"]]:
    time_horizon, control_dimension = around.shape

    key, subkey = jrandom.split(key)
    samples = around[..., None] + standard_deviation[None, :, None] * jrandom.normal(
        subkey, shape=(time_horizon, control_dimension, rollout_count)
    )

    return key, samples
