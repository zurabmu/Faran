import asyncio

from faran.numpy import model, sampler, types
from faran_visualizer import Scene, render, visualizer

KNOT_COUNT = 4  # Spline knots over the horizon. Try 2 or 15.
HORIZON = 30

halton = sampler.halton(
    standard_deviation=[0.5, 0.2],
    rollout_count=64,
    knot_count=KNOT_COUNT,
    to_batch=types.bicycle.control_input_batch.create,
    seed=42,
)
bicycle = model.bicycle.dynamical(
    time_step_size=0.1, wheelbase=2.5, steering_limits=(-0.5, 0.5)
)
samples = halton.sample(
    around=types.bicycle.control_input_sequence.zeroes(horizon=HORIZON)
)
rollouts = bicycle.simulate(
    inputs=samples,
    initial_state=types.bicycle.state.create(x=0.0, y=0.0, heading=0.0, speed=5.0),
).positions

asyncio.run(
    visualizer.simulation()(
        Scene(
            time_step=0.1,
            step_count=1,
            background=[
                render.lines(
                    name="rollouts",
                    label="Rollouts",
                    strips=[
                        rollouts.array[:, :, m] for m in range(rollouts.rollout_count)
                    ],
                    color="#a3a6ff99",
                    width=1.0,
                )
            ],
        ),
        key="halton",
    )
)
