import asyncio

import numpy as np
from faran.numpy import extract, filters, model, mppi, sampler, trajectory, types
from faran_visualizer import Plot, Scene, render, visualizer

TEMPERATURE = 50.0  # Try 5.0 or 5000.0.
HORIZON = 30
STEPS = 60


class RecordingSampler:
    """Passes the samples through and keeps the last batch, to draw the rollouts."""

    def __init__(self, inner):
        self.inner, self.last = inner, None

    def sample(self, *, around):
        self.last = self.inner.sample(around=around)
        return self.last

    @property
    def rollout_count(self):
        return self.inner.rollout_count


bicycle = model.bicycle.dynamical(
    time_step_size=0.1,
    wheelbase=2.5,
    speed_limits=(0.0, 15.0),
    steering_limits=(-0.5, 0.5),
    acceleration_limits=(-3.0, 3.0),
)
recording = RecordingSampler(
    sampler.gaussian(
        standard_deviation=[0.5, 0.2],
        rollout_count=256,
        to_batch=types.bicycle.control_input_batch.create,
        seed=42,
    )
)
reference = trajectory.waypoints(
    points=[(0.0, 0.0), (10.0, 0.0), (20.0, 10.0), (10.0, 20.0), (0.0, 20.0)],
    path_length=30.0,
)
planner, augmented_model, _, _ = mppi.mpcc(
    model=bicycle,
    sampler=recording,
    reference=reference,
    position_extractor=extract.from_physical(lambda states: states.positions),
    config={"weights": {"contouring": 50.0, "lag": 100.0, "progress": 1000.0}},
    filter_function=filters.savgol(window_length=11, polynomial_order=3),
)

state = types.augmented.state.of(
    physical=types.bicycle.state.create(x=0.0, y=0.0, heading=0.0, speed=0.0),
    virtual=types.simple.state.zeroes(dimension=1),
)
nominal = types.augmented.control_input_sequence.of(
    physical=types.bicycle.control_input_sequence.zeroes(horizon=HORIZON),
    virtual=types.simple.control_input_sequence.zeroes(horizon=HORIZON, dimension=1),
)
positions, rollouts, heavy, plans = [], [], [], []
for _ in range(STEPS):
    control = planner.step(
        temperature=TEMPERATURE, nominal_input=nominal, initial_state=state
    )
    weights = np.asarray(control.debug.trajectory_weights.array)
    positions.append(np.array([state.physical.x, state.physical.y]))
    rollouts.append(
        bicycle.simulate(
            inputs=recording.last, initial_state=state.physical
        ).positions.array
    )
    heavy.append(weights > 1.0 / len(weights))
    plan = bicycle.forward(inputs=control.optimal.physical, state=state.physical)
    plans.append(np.column_stack([plan.x(), plan.y()]))
    nominal = control.nominal
    state = augmented_model.step(inputs=control.optimal, state=state)

path = reference.query(
    types.path_parameters(np.linspace(0, 30, 200)[:, None])
).positions

asyncio.run(
    visualizer.simulation()(
        Scene(
            time_step=0.1,
            step_count=STEPS,
            background=[
                render.lines(
                    name="reference",
                    label="Reference path",
                    strips=[path[:, :, 0]],
                    color="#f1e4ecaa",
                )
            ],
            at_step=lambda step: [
                render.lines(
                    name="rollouts/light",
                    label="Rollouts at or below average weight",
                    strips=[
                        rollouts[step][:, :, m] for m in np.flatnonzero(~heavy[step])
                    ],
                    color="#7f83f040",
                    width=1.0,
                ),
                render.lines(
                    name="rollouts/heavy",
                    label="Rollouts above average weight",
                    strips=[
                        rollouts[step][:, :, m] for m in np.flatnonzero(heavy[step])
                    ],
                    color="#ffa487",
                    width=1.0,
                ),
                render.lines(
                    name="optimal plan",
                    label="Optimal plan",
                    strips=[plans[step]],
                    color="#a3a6ff",
                    width=3.0,
                ),
                render.dots(
                    name="vehicle",
                    label="Vehicle",
                    positions=positions[step][None],
                    color="#ffd2c2",
                    size=8.0,
                ),
            ],
            plots=[
                Plot.line(
                    name="Rollouts above average weight",
                    values=np.array([mask.sum() for mask in heavy], dtype=float),
                )
            ],
        ),
        key="rollouts",
    )
)
