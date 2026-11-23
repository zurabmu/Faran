from typing import Self
from dataclasses import dataclass

from faran.types import Array, jaxtyped, NumPyObstacleSimulator
from faran.obstacles.basic import NumPyObstacle2dPosesForTimeStep

from jaxtyping import Float

import numpy as np


@jaxtyped
@dataclass(frozen=True)
class NumPyStaticObstacleSimulator(
    NumPyObstacleSimulator[NumPyObstacle2dPosesForTimeStep]
):
    """Simulates stationary obstacles by replicating fixed positions over the horizon."""

    positions: Float[Array, "K 2"]
    headings: Float[Array, " K"]

    @staticmethod
    def empty() -> "NumPyStaticObstacleSimulator":
        positions = np.empty((0, 2))

        return NumPyStaticObstacleSimulator.create(positions=positions)

    @staticmethod
    def create(
        *, positions: Float[Array, "K 2"], headings: Float[Array, " K"] | None = None
    ) -> "NumPyStaticObstacleSimulator":
        """Creates a simulator of obstacles that do not move.

        Args:
            positions: Position of each obstacle, in meters.
            headings: Heading of each obstacle, in radians. Without headings, all
                headings are zero.
        """
        count = positions.shape[0]
        headings = headings if headings is not None else np.zeros(shape=(count,))

        return NumPyStaticObstacleSimulator(positions=positions, headings=headings)

    def with_time_step_size(self, time_step_size: float) -> Self:
        # Time step does not matter.
        return self

    def step(self) -> NumPyObstacle2dPosesForTimeStep:
        return NumPyObstacle2dPosesForTimeStep.create(
            x=self.positions[:, 0],
            y=self.positions[:, 1],
            heading=self.headings,
        )

    @property
    def obstacle_count(self) -> int:
        return self.positions.shape[0]
