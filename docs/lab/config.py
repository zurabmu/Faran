from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class LabConfig:
    horizon: int
    time_step: float
    wheelbase: float
    temperature: float
    vehicle_length: float
    vehicle_width: float
    reference_sample_count: int
    circle_offsets: tuple[float, ...]
    circle_radius: float


CONFIG: Final = LabConfig(
    horizon=30,
    time_step=0.1,
    wheelbase=2.5,
    temperature=50.0,
    vehicle_length=4.0,
    vehicle_width=1.6,
    reference_sample_count=200,
    circle_offsets=(-0.5, 0.0, 0.5),
    circle_radius=0.8,
)


@dataclass(frozen=True)
class NavigationConfig:
    time_step: float
    horizon: int
    rollout_count: int
    rollouts_drawn: int
    temperature: float
    speed_limits: tuple[float, float]
    turn_rate_limits: tuple[float, float]
    noise: tuple[float, float]
    goal_weight: float
    terminal_weight: float
    obstacle_weight: float
    obstacle_margin: float
    speed_weight: float
    arrival_distance: float
    step_limit: int
    trail_lifetime: int
    taken_color: str
    plan_color: str
    rollout_color: str
    obstacle_color: str


NAVIGATION_CONFIG: Final = NavigationConfig(
    time_step=0.05,
    horizon=60,
    rollout_count=128,
    rollouts_drawn=64,
    temperature=0.5,
    speed_limits=(0.0, 2.4),
    turn_rate_limits=(-2.6, 2.6),
    noise=(0.45, 0.8),
    goal_weight=0.6,
    terminal_weight=12.0,
    obstacle_weight=400.0,
    obstacle_margin=0.25,
    speed_weight=0.4,
    arrival_distance=0.3,
    step_limit=600,
    trail_lifetime=66,
    taken_color="#ffa487",
    plan_color="#a3a6ff",
    rollout_color="#a3a6ff12",
    obstacle_color="#3e3650",
)
