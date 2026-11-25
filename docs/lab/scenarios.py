from math import pi
from typing import Final

import numpy as np

from faran.numpy import boundary, costs, obstacles, trajectory

from .avoidance import circle_distance, obstacle_provider
from .config import CONFIG
from .planner import control_smoothing, mpcc_planner, position_extractor
from .scene import corridor_of, no_corridor, obstacle_circles, scene_of
from .simulation import Simulation


def path_following() -> Simulation:
    reference = trajectory.waypoints(
        points=[
            (0.0, 0.0),
            (10.0, 0.0),
            (20.0, 10.0),
            (10.0, 20.0),
            (0.0, 20.0),
            (-10.0, 20.0),
            (-20.0, 30.0),
            (-10.0, 40.0),
            (0.0, 40.0),
        ],
        path_length=50.0,
    )
    planner, dynamics = mpcc_planner(
        reference=reference,
        rollout_count=256,
        cost_terms=(),
        minimum_progress_speed=0.0,
    )
    return Simulation(
        planner=planner,
        dynamics=dynamics,
        scene=scene_of(reference, corridor=no_corridor(), obstacles=[]),
        goal_progress=0.9 * reference.path_length,
        step_limit=150,
        observe_obstacles=no_obstacles,
    )


def corridor() -> Simulation:
    reference = trajectory.waypoints(
        points=[
            (0.0, 0.0),
            (10.0, 0.0),
            (20.0, 0.0),
            (20.0, 5.0),
            (15.0, 10.0),
            (15.0, 15.0),
            (10.0, 20.0),
        ],
        path_length=50.0,
    )
    walls = boundary.fixed_width(
        reference=reference,
        position_extractor=position_extractor(),
        left=1.5,
        right=1.5,
    )
    planner, dynamics = mpcc_planner(
        reference=reference,
        rollout_count=256,
        cost_terms=(
            control_smoothing(),
            costs.safety.boundary(
                distance=walls, distance_threshold=1.0, weight=1000.0
            ),
        ),
        minimum_progress_speed=0.0,
    )
    return Simulation(
        planner=planner,
        dynamics=dynamics,
        scene=scene_of(reference, corridor=corridor_of(walls), obstacles=[]),
        goal_progress=0.9 * reference.path_length,
        step_limit=150,
        observe_obstacles=no_obstacles,
    )


def obstacle_avoidance() -> Simulation:
    positions = ((20.0, 2.5), (35.0, 7.5), (50.0, 2.5))
    headings = (0.0, pi / 4, -pi / 6)
    reference = trajectory.waypoints(
        points=[(0.0, 0.0), (15.0, 0.0), (30.0, 5.0), (45.0, 5.0), (60.0, 0.0)],
        path_length=70.0,
    )
    simulator = obstacles.static(
        positions=np.array(positions), headings=np.array(headings)
    ).with_time_step_size(CONFIG.time_step)
    provider = obstacle_provider(obstacle_count=simulator.obstacle_count)
    walls = boundary.fixed_width(
        reference=reference,
        position_extractor=position_extractor(),
        left=3.0,
        right=3.0,
    )
    planner, dynamics = mpcc_planner(
        reference=reference,
        rollout_count=512,
        cost_terms=(
            control_smoothing(),
            costs.safety.collision(
                obstacle_states=provider,
                sampler=obstacles.sampler.gaussian(seed=44),
                distance=circle_distance(),
                distance_threshold=np.full(len(CONFIG.circle_offsets), 0.5),
                weight=1500.0,
            ),
            costs.safety.boundary(
                distance=walls, distance_threshold=0.25, weight=1000.0
            ),
        ),
        minimum_progress_speed=1.0,
    )
    return Simulation(
        planner=planner,
        dynamics=dynamics,
        scene=scene_of(
            reference,
            corridor=corridor_of(walls),
            obstacles=obstacle_circles(positions=positions, headings=headings),
        ),
        goal_progress=0.7 * reference.path_length,
        step_limit=350,
        observe_obstacles=lambda: provider.observe(simulator.step()),
    )


def no_obstacles() -> None:
    pass


demos: Final = {
    "path-following": path_following,
    "corridor": corridor,
    "obstacle-avoidance": obstacle_avoidance,
}
