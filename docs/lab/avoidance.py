import numpy as np

from faran import Circles
from faran.numpy import distance, extract, model, obstacles, predictor, types

from .config import CONFIG
from .planner import position_extractor, vehicle_headings


def obstacle_provider(*, obstacle_count: int):
    """Tracks observed obstacles and predicts their motion over the horizon."""
    return obstacles.provider.predicting(
        predictor=predictor.curvilinear(
            horizon=CONFIG.horizon,
            model=model.bicycle.obstacle(
                time_step_size=CONFIG.time_step, wheelbase=CONFIG.wheelbase
            ),
            estimator=model.bicycle.estimator.finite_difference(
                time_step_size=CONFIG.time_step, wheelbase=CONFIG.wheelbase
            ),
            prediction=BicyclePredictionCreator(),
        ),
        history=types.obstacle_states_running_history.empty(
            creator=types.obstacle_2d_poses,
            horizon=2,
            obstacle_count=obstacle_count,
        ),
        id_assignment=obstacles.id_assignment.hungarian(
            position_extractor=ObstaclePositionExtractor(),
            cutoff=10.0,
        ),
    )


def circle_distance():
    """Distance between the vehicle and the obstacles, each covered by the same circles."""
    circles = Circles(
        origins=np.array([(offset, 0.0) for offset in CONFIG.circle_offsets]),
        radii=np.full(len(CONFIG.circle_offsets), CONFIG.circle_radius),
    )
    return distance.circles(
        ego=circles,
        obstacle=circles,
        position_extractor=position_extractor(),
        heading_extractor=extract.from_physical(vehicle_headings),
        obstacle_position_extractor=obstacle_positions,
        obstacle_heading_extractor=obstacle_headings,
    )


class BicyclePredictionCreator:
    def __call__(
        self, *, states: types.bicycle.ObstacleStateSequences
    ) -> types.Obstacle2dPoses:
        return states.pose()

    def empty(self, *, horizon: int) -> types.Obstacle2dPoses:
        return types.obstacle_2d_poses.empty(horizon=horizon)


class ObstaclePositionExtractor:
    def of_states_for_time_step(
        self, states: types.Obstacle2dPosesForTimeStep, /
    ) -> types.Obstacle2dPositionsForTimeStep:
        return states.positions()

    def of_states(self, states: types.Obstacle2dPoses, /) -> types.Obstacle2dPositions:
        return states.positions()


def obstacle_positions(
    states: types.SampledObstacle2dPoses,
) -> types.SampledObstaclePositions:
    return states.positions()


def obstacle_headings(
    states: types.SampledObstacle2dPoses,
) -> types.SampledObstacleHeadings:
    return states.headings()
