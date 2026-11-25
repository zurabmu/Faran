from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Protocol

import msgspec

import numpy as np

from faran import DynamicalModel, Mppi, Sampler
from faran.numpy import costs, model, mppi, sampler, types
from faran_visualizer import CanvasRenderer, Rendering, render

from .config import NAVIGATION_CONFIG
from .arrays import Position, Positions, Radii
from .trail import Trail

type State = types.unicycle.State
type Inputs = types.unicycle.ControlInputSequence
type Unicycle = DynamicalModel[
    State,
    types.unicycle.StateSequence,
    types.unicycle.StateBatch,
    Inputs,
    types.unicycle.ControlInputBatch,
]


class LayoutStart(msgspec.Struct, frozen=True):
    x: float
    y: float
    heading: float


class LayoutObstacle(msgspec.Struct, frozen=True):
    center: tuple[float, float]
    radius: float


class Layout(msgspec.Struct, frozen=True):
    places: list[tuple[float, float]]
    obstacles: list[LayoutObstacle]
    start: LayoutStart


class MotionFrames(msgspec.Struct, frozen=True):
    start: msgspec.Raw
    end: msgspec.Raw


class Step(msgspec.Struct, frozen=True):
    frame: msgspec.Raw
    motion: MotionFrames
    moving: bool
    fading: bool


@dataclass(frozen=True)
class Circles:
    centers: Positions
    radii: Radii


@dataclass(frozen=True)
class GoalCost:
    """Squared distance of each state to the goal, weighted more at the end of the horizon."""

    goal: Position

    def __call__(
        self,
        *,
        inputs: types.unicycle.ControlInputBatch,
        states: types.unicycle.StateBatch,
    ) -> types.simple.Costs:
        positions = states.positions.array
        distances = np.sum((positions - self.goal[None, :, None]) ** 2, axis=1)
        weights = np.full(states.horizon, NAVIGATION_CONFIG.goal_weight)
        weights[-1] += NAVIGATION_CONFIG.terminal_weight
        return types.simple.costs(weights[:, None] * distances)


@dataclass(frozen=True)
class ObstacleCost:
    """Squared intrusion of each state into a margin around circular obstacles."""

    obstacles: Circles

    def __call__(
        self,
        *,
        inputs: types.unicycle.ControlInputBatch,
        states: types.unicycle.StateBatch,
    ) -> types.simple.Costs:
        positions = states.positions.array
        offsets = positions[:, :, None, :] - self.obstacles.centers.T[None, :, :, None]
        distances = np.sqrt(np.sum(offsets**2, axis=1))
        intrusion = np.maximum(
            0.0,
            self.obstacles.radii[None, :, None]
            + NAVIGATION_CONFIG.obstacle_margin
            - distances,
        )
        return types.simple.costs(
            NAVIGATION_CONFIG.obstacle_weight * np.sum(intrusion**2, axis=1)
        )


@dataclass
class RecordingSampler:
    """Samples like the Gaussian sampler and keeps every batch it sampled."""

    batches: list[types.unicycle.ControlInputBatch] = field(default_factory=list)
    inner: Sampler[Inputs, types.unicycle.ControlInputBatch] = field(
        default_factory=lambda: sampler.gaussian(
            standard_deviation=list(NAVIGATION_CONFIG.noise),
            rollout_count=NAVIGATION_CONFIG.rollout_count,
            to_batch=types.unicycle.control_input_batch.create,
            seed=0,
        )
    )

    def sample(self, *, around: Inputs) -> types.unicycle.ControlInputBatch:
        self.batches.append(self.inner.sample(around=around))
        return self.batches[-1]

    @property
    def rollout_count(self) -> int:
        return self.inner.rollout_count


class Motion(Protocol):
    @property
    def moving(self) -> bool:
        """Whether `step` changes the state."""
        ...

    def step(self, state: State) -> tuple[State, Sequence[Rendering]]:
        """Returns the next state and the renderings of the planning."""
        ...


class Resting:
    """The unicycle stays where it is."""

    @property
    def moving(self) -> bool:
        return False

    def step(self, state: State) -> tuple[State, Sequence[Rendering]]:
        return state, []


@dataclass
class Driving:
    """The unicycle drives towards a goal, replanning with MPPI at every step."""

    goal: Position
    dynamics: Unicycle
    planner: Mppi[State, Inputs]
    recording: RecordingSampler
    nominal: Inputs
    steps: int = 0
    arrived: bool = False

    @staticmethod
    def towards(goal: Position, *, obstacles: Circles) -> "Driving":
        dynamics = unicycle()
        recording = RecordingSampler()
        return Driving(
            goal=goal,
            dynamics=dynamics,
            planner=mppi.base(
                model=dynamics,
                cost_function=costs.combined(
                    GoalCost(goal=goal),
                    ObstacleCost(obstacles=obstacles),
                    costs.comfort.control_effort(
                        weights=np.array([NAVIGATION_CONFIG.speed_weight, 0.0])
                    ),
                ),
                sampler=recording,
            ),
            recording=recording,
            nominal=types.unicycle.control_input_sequence.zeroes(
                horizon=NAVIGATION_CONFIG.horizon
            ),
        )

    @property
    def moving(self) -> bool:
        return not self.arrived and self.steps < NAVIGATION_CONFIG.step_limit

    def step(self, state: State) -> tuple[State, Sequence[Rendering]]:
        control = self.planner.step(
            temperature=NAVIGATION_CONFIG.temperature,
            nominal_input=self.nominal,
            initial_state=state,
        )
        next_state = self.dynamics.step(control.optimal, state)
        self.record_step(nominal=control.nominal, reached=next_state)
        return next_state, [
            self.rollout_lines(state),
            self.plan_line(state, optimal=control.optimal),
        ]

    def record_step(self, *, nominal: Inputs, reached: State) -> None:
        self.nominal = nominal
        self.steps += 1
        self.arrived = distance(reached, self.goal) < NAVIGATION_CONFIG.arrival_distance

    def rollout_lines(self, state: State) -> Rendering:
        rollouts = self.dynamics.simulate(
            inputs=self.recording.batches[-1], initial_state=state
        )
        return render.lines(
            name="rollouts",
            label="Rollouts",
            strips=[
                path_from(state, rollouts.rollout(index))
                for index in range(NAVIGATION_CONFIG.rollouts_drawn)
            ],
            color=NAVIGATION_CONFIG.rollout_color,
            width=1.0,
        )

    def plan_line(self, state: State, *, optimal: Inputs) -> Rendering:
        plan = self.dynamics.forward(optimal, state)
        return render.lines(
            name="plan",
            label="Optimal plan",
            strips=[path_from(state, plan)],
            color=NAVIGATION_CONFIG.plan_color,
            width=1.5,
            pattern="dashed",
        )


@dataclass
class Navigation:
    """Drives a unicycle across the docs map with Faran's MPPI planner. Each call to
    `advance` runs one planner step and returns the frame to draw as JSON."""

    places: Positions
    obstacles: Circles
    state: State
    motion: Motion = field(default_factory=Resting)
    trail: Trail = field(default_factory=Trail)
    step_index: int = 0

    @staticmethod
    def from_layout(layout_json: str) -> "Navigation":
        """Creates the navigation for the docs map layout, given as JSON with the
        `places`, `obstacles` and `start` of the map in field units."""
        layout = msgspec.json.decode(layout_json, type=Layout)
        start = layout.start
        return Navigation(
            places=np.array(layout.places, dtype=float),
            obstacles=Circles(
                centers=np.array([it.center for it in layout.obstacles], dtype=float),
                radii=np.array([it.radius for it in layout.obstacles], dtype=float),
            ),
            state=types.unicycle.state.create(
                x=start.x, y=start.y, heading=start.heading
            ),
        )

    def background(self) -> str:
        """Returns the obstacles as a frame in JSON."""
        angles = np.linspace(0.0, 2.0 * np.pi, 49)
        circles = [
            np.column_stack([x + r * np.cos(angles), y + r * np.sin(angles)])
            for (x, y), r in zip(self.obstacles.centers, self.obstacles.radii)
        ]
        return CanvasRenderer.frame_json(
            renderings=[
                render.lines(
                    name="obstacles",
                    label="Obstacles",
                    strips=circles,
                    color=NAVIGATION_CONFIG.obstacle_color,
                    width=1.0,
                    pattern="dashed",
                )
            ]
        )

    def aim(self, place: int) -> None:
        """Starts planning towards the place with the given index."""
        self.motion = Driving.towards(self.places[place], obstacles=self.obstacles)

    def advance(self) -> str:
        """Runs one planner step towards the place aimed at, unless the unicycle has
        stopped, and returns the step as JSON."""
        self.step_index += 1
        moved = self.motion.moving
        start = position_of(self.state)
        planning = self.drive(start) if moved else []
        self.trail.forget_faded(now=self.step_index)
        return msgspec.json.encode(
            self.step(start, planning=planning, moved=moved)
        ).decode()

    def drive(self, start: Position) -> Sequence[Rendering]:
        self.state, planning = self.motion.step(self.state)
        self.trail.extend(
            start=start, end=position_of(self.state), step=self.step_index
        )
        return planning

    def step(
        self, start: Position, *, planning: Sequence[Rendering], moved: bool
    ) -> Step:
        return Step(
            frame=frame_of(
                [
                    *(planning if self.motion.moving else []),
                    *self.trail.settled_renderings(now=self.step_index, growing=moved),
                ]
            ),
            motion=MotionFrames(
                start=self.motion_frame(start, moved=moved),
                end=self.motion_frame(position_of(self.state), moved=moved),
            ),
            moving=self.motion.moving,
            fading=self.trail.fading,
        )

    def motion_frame(self, position: Position, *, moved: bool) -> msgspec.Raw:
        return frame_of(
            [
                *(self.trail.head_renderings(position) if moved else []),
                render.dots(
                    name="unicycle",
                    label="Robot",
                    positions=position[None, :],
                    color=NAVIGATION_CONFIG.taken_color,
                    size=8.0,
                ),
            ]
        )


def unicycle() -> Unicycle:
    return model.unicycle.dynamical(
        time_step_size=NAVIGATION_CONFIG.time_step,
        speed_limits=NAVIGATION_CONFIG.speed_limits,
        angular_velocity_limits=NAVIGATION_CONFIG.turn_rate_limits,
    )


def distance(state: State, goal: Position) -> float:
    return float(np.linalg.norm(position_of(state) - goal))


def position_of(state: State) -> Position:
    return np.array([state.x, state.y])


def path_from(state: State, states: types.unicycle.StateSequence) -> Positions:
    return np.vstack([position_of(state), np.column_stack([states.x(), states.y()])])


def frame_of(renderings: Sequence[Rendering]) -> msgspec.Raw:
    return msgspec.Raw(CanvasRenderer.frame_json(renderings=renderings))
