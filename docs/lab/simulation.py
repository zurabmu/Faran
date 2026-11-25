from collections.abc import Callable, Sequence
from time import perf_counter

import msgspec
import numpy as np
from numpy.typing import ArrayLike

from faran.numpy import types
from faran_visualizer import CanvasRenderer, Rendering

from .config import CONFIG
from .planner import AugmentedInputs, AugmentedState, Dynamics, Planner
from .scene import moving_parts


class Step(msgspec.Struct, frozen=True, rename="camel"):
    frame: msgspec.Raw
    step: int
    speed: float
    progress: float
    planning_milliseconds: float
    reached_goal: bool
    finished: bool


class Simulation:
    """Closed-loop MPCC simulation that a caller advances one planner step at a time."""

    def __init__(
        self,
        *,
        planner: Planner,
        dynamics: Dynamics,
        scene: Sequence[Rendering],
        goal_progress: float,
        step_limit: int,
        observe_obstacles: Callable[[], None],
    ) -> None:
        self.planner = planner
        self.dynamics = dynamics
        self.scene = scene
        self.goal_progress = goal_progress
        self.step_limit = step_limit
        self.observe_obstacles = observe_obstacles
        self.step_index = 0
        self.state: AugmentedState = types.augmented.state.of(
            physical=types.bicycle.state.create(x=0.0, y=0.0, heading=0.0, speed=0.0),
            virtual=types.simple.state.zeroes(dimension=1),
        )
        self.nominal: AugmentedInputs = types.augmented.control_input_sequence.of(
            physical=types.bicycle.control_input_sequence.zeroes(
                horizon=CONFIG.horizon
            ),
            virtual=types.simple.control_input_sequence.zeroes(
                horizon=CONFIG.horizon, dimension=1
            ),
        )
        self.driven: list[list[float]] = [[0.0, 0.0]]

    def background(self) -> str:
        """Returns the parts of the demo that do not move as a frame of the canvas engine
        in JSON, with positions in meters."""
        return CanvasRenderer.frame_json(renderings=self.scene)

    def advance(self) -> str:
        """Runs one planner step and returns the step as JSON, with the moving parts as
        a frame of the canvas engine."""
        started_at = perf_counter()
        control = self.planner.step(
            temperature=CONFIG.temperature,
            nominal_input=self.nominal,
            initial_state=self.state,
        )
        planning_time = perf_counter() - started_at
        plan = self.dynamics.forward(control.optimal, self.state)

        self.nominal = control.nominal
        self.state = self.dynamics.step(control.optimal, self.state)
        self.observe_obstacles()
        self.step_index += 1
        return msgspec.json.encode(
            self.step(plan=plan, planning_time=planning_time)
        ).decode()

    def step(self, *, plan: ArrayLike, planning_time: float) -> Step:
        x, y, heading, speed, progress = np.asarray(self.state).tolist()
        self.driven.append([x, y])
        reached_goal = progress >= self.goal_progress
        return Step(
            frame=msgspec.Raw(
                CanvasRenderer.frame_json(
                    renderings=moving_parts(
                        driven=np.asarray(self.driven),
                        plan=np.asarray(plan)[:, :2],
                        x=x,
                        y=y,
                        heading=heading,
                    )
                )
            ),
            step=self.step_index,
            speed=round(speed, 2),
            progress=round(min(progress / self.goal_progress, 1.0), 4),
            planning_milliseconds=round(planning_time * 1000, 1),
            reached_goal=reached_goal,
            finished=reached_goal or self.step_index >= self.step_limit,
        )
