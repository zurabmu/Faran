import asyncio

from faran.numpy import model, sampler, types
from faran_visualizer import Scene, render, visualizer

STANDARD_DEVIATION = [0.5, 0.2]  # Acceleration and steering angle. Try [0.5, 0.05].
HORIZON = 30

gaussian = sampler.gaussian(
    standard_deviation=STANDARD_DEVIATION,
    rollout_count=64,
    to_batch=types.bicycle.control_input_batch.create,
    seed=42,
)
bicycle = model.bicycle.dynamical(
    time_step_size=0.1, wheelbase=2.5, steering_limits=(-0.5, 0.5)
)
samples = gaussian.sample(
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
        key="gaussian",
    )
)
