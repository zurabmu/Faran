from dataclasses import dataclass

from faran.types import (
    jaxtyped,
    DistanceExtractor,
    JaxPositionExtractor,
    JaxHeadingExtractor,
    JaxSampledObstaclePositions,
    JaxSampledObstaclePositionExtractor,
    JaxSampledObstacleHeadingExtractor,
)
from faran.costs.collision import JaxDistance
from faran.costs.distance.accelerated import replace_missing
from faran.costs.distance.circles.common import Circles

from jaxtyping import Array as JaxArray, Float

import jax
import jax.numpy as jnp


@dataclass(frozen=True)
class JaxCircleDistanceExtractor[StateT, SampledObstacleStatesT](
    DistanceExtractor[StateT, SampledObstacleStatesT, JaxDistance]
):
    """
    Computes the distances between parts of the ego robot and obstacles. Both the ego
    and the obstacles are represented as collections of circles.
    """

    ego_origins: Float[JaxArray, "V 2"]
    ego_radii: Float[JaxArray, " V"]
    obstacle_origins: Float[JaxArray, "C 2"]
    obstacle_radii: Float[JaxArray, " C"]
    positions_from: JaxPositionExtractor[StateT]
    headings_from: JaxHeadingExtractor[StateT]
    obstacle_positions_from: JaxSampledObstaclePositionExtractor[SampledObstacleStatesT]
    obstacle_headings_from: JaxSampledObstacleHeadingExtractor[SampledObstacleStatesT]

    @staticmethod
    def create[S, SOS](
        *,
        ego: Circles,
        obstacle: Circles,
        position_extractor: JaxPositionExtractor[S],
        heading_extractor: JaxHeadingExtractor[S],
        obstacle_position_extractor: JaxSampledObstaclePositionExtractor[SOS],
        obstacle_heading_extractor: JaxSampledObstacleHeadingExtractor[SOS],
    ) -> "JaxCircleDistanceExtractor[S, SOS]":
        return JaxCircleDistanceExtractor(
            ego_origins=jnp.asarray(ego.origins),
            ego_radii=jnp.asarray(ego.radii),
            obstacle_origins=jnp.asarray(obstacle.origins),
            obstacle_radii=jnp.asarray(obstacle.radii),
            positions_from=position_extractor,
            headings_from=heading_extractor,
            obstacle_positions_from=obstacle_position_extractor,
            obstacle_headings_from=obstacle_heading_extractor,
        )

    def __call__(
        self, *, states: StateT, obstacle_states: SampledObstacleStatesT
    ) -> JaxDistance:
        ego_positions = self.positions_from(states)
        ego_headings = self.headings_from(states)
        obstacle_positions = self.obstacle_positions_from(obstacle_states)
        obstacle_headings = self.obstacle_headings_from(obstacle_states)

        if self._no_obstacles_exist(obstacle_positions):
            T, M = ego_positions.horizon, ego_positions.rollout_count
            V = self._ego_circle_count
            N = obstacle_positions.sample_count
            return JaxDistance(jnp.full((T, V, M, N), jnp.inf))

        return JaxDistance(
            compute_circle_distances(
                ego_x=ego_positions.x_array,
                ego_y=ego_positions.y_array,
                ego_heading=ego_headings.heading_array,
                ego_origins=self.ego_origins,
                ego_radii=self.ego_radii,
                obstacle_x=obstacle_positions.x_array,
                obstacle_y=obstacle_positions.y_array,
                obstacle_heading=obstacle_headings.heading_array,
                obstacle_origins=self.obstacle_origins,
                obstacle_radii=self.obstacle_radii,
            )
        )

    def _no_obstacles_exist(self, positions: JaxSampledObstaclePositions) -> bool:
        return self._obstacle_circle_count == 0 or positions.x_array.shape[1] == 0

    @property
    def _obstacle_circle_count(self) -> int:
        return self.obstacle_origins.shape[0]

    @property
    def _ego_circle_count(self) -> int:
        return self.ego_origins.shape[0]


@jax.jit
@jaxtyped
def compute_circle_distances(
    *,
    ego_x: Float[JaxArray, "T M"],
    ego_y: Float[JaxArray, "T M"],
    ego_heading: Float[JaxArray, "T M"],
    ego_origins: Float[JaxArray, "V 2"],
    ego_radii: Float[JaxArray, " V"],
    obstacle_x: Float[JaxArray, "T K N"],
    obstacle_y: Float[JaxArray, "T K N"],
    obstacle_heading: Float[JaxArray, "T K N"],
    obstacle_origins: Float[JaxArray, "C 2"],
    obstacle_radii: Float[JaxArray, " C"],
) -> Float[JaxArray, "T V M N"]:
    ego_global_x, ego_global_y = to_global_positions(
        x=ego_x, y=ego_y, heading=ego_heading, local_origins=ego_origins
    )

    obstacle_global_x, obstacle_global_y = to_global_positions(
        x=obstacle_x,
        y=obstacle_y,
        heading=obstacle_heading,
        local_origins=obstacle_origins,
    )

    obstacle_x, obstacle_y, obstacle_radii = flatten_obstacle_circles(
        obstacle_x=obstacle_global_x,
        obstacle_y=obstacle_global_y,
        obstacle_radii=obstacle_radii,
    )

    return min_distances_to_obstacle_circles(
        ego_x=ego_global_x,
        ego_y=ego_global_y,
        ego_radii=ego_radii,
        obstacle_x=obstacle_x,
        obstacle_y=obstacle_y,
        obstacle_radii=obstacle_radii,
    ).transpose(1, 0, 2, 3)


@jaxtyped
def flatten_obstacle_circles(
    *,
    obstacle_x: Float[JaxArray, "C T K N"],
    obstacle_y: Float[JaxArray, "C T K N"],
    obstacle_radii: Float[JaxArray, " C"],
) -> tuple[
    Float[JaxArray, "CK T N"],
    Float[JaxArray, "CK T N"],
    Float[JaxArray, " CK"],
]:
    T, N = obstacle_x.shape[1], obstacle_x.shape[3]
    K = obstacle_x.shape[2]
    flat_x = obstacle_x.transpose(0, 2, 1, 3).reshape(-1, T, N)
    flat_y = obstacle_y.transpose(0, 2, 1, 3).reshape(-1, T, N)
    flat_radii = jnp.repeat(obstacle_radii, K)
    return flat_x, flat_y, flat_radii


@jaxtyped
def min_distances_to_obstacle_circles(
    *,
    ego_x: Float[JaxArray, "V T M"],
    ego_y: Float[JaxArray, "V T M"],
    ego_radii: Float[JaxArray, " V"],
    obstacle_x: Float[JaxArray, "CK T N"],
    obstacle_y: Float[JaxArray, "CK T N"],
    obstacle_radii: Float[JaxArray, " CK"],
) -> Float[JaxArray, "V T M N"]:
    # NOTE: XLA compiles a min reduction over the obstacle circle axis inefficiently, and
    # much more so when it fuses the reduction with the cost that uses the distances.
    # Scanning over the obstacle circles and keeping the running minimum avoids the
    # reduction altogether.
    def keep_closer(
        closest: Float[JaxArray, "V T M N"],
        circle: tuple[
            Float[JaxArray, "T N"], Float[JaxArray, "T N"], Float[JaxArray, ""]
        ],
    ) -> tuple[Float[JaxArray, "V T M N"], None]:
        x, y, radius = circle
        dx = ego_x[:, :, :, None] - x[None, :, None, :]
        dy = ego_y[:, :, :, None] - y[None, :, None, :]
        distance = jnp.sqrt(dx**2 + dy**2) - (ego_radii[:, None, None, None] + radius)
        return jnp.minimum(closest, distance), None

    V, T, M = ego_x.shape
    N = obstacle_x.shape[2]
    closest, _ = jax.lax.scan(
        keep_closer,
        jnp.full((V, T, M, N), jnp.inf),
        (obstacle_x, obstacle_y, obstacle_radii),
    )
    return closest


@jax.jit
@jaxtyped
def to_global_positions(
    *,
    x: Float[JaxArray, " T *S"],
    y: Float[JaxArray, " T *S"],
    heading: Float[JaxArray, " T *S"],
    local_origins: Float[JaxArray, "L 2"],
) -> tuple[Float[JaxArray, "L T *S"], Float[JaxArray, "L T *S"]]:
    x, y, heading = replace_missing(x=x, y=y, heading=heading)

    shape = (-1,) + (1,) * x.ndim
    local_x = local_origins[:, 0].reshape(shape)
    local_y = local_origins[:, 1].reshape(shape)

    cos_h, sin_h = jnp.cos(heading), jnp.sin(heading)

    return (
        x + local_x * cos_h - local_y * sin_h,
        y + local_x * sin_h + local_y * cos_h,
    )
