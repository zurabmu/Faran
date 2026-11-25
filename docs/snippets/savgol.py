import asyncio

import numpy as np
from faran.numpy import filters, model, sampler, types
from faran_visualizer import Plot, Scene, render, visualizer

WINDOW_LENGTH = 11  # Odd number of time steps. Try 5 or 21.
POLYNOMIAL_ORDER = 3  # Less than the window length. Try 1.
STEPS = 60

noisy = sampler.gaussian(
    standard_deviation=[0.3, 0.1],
    rollout_count=1,
    to_batch=types.bicycle.control_input_batch.create,
    seed=7,
).sample(around=types.bicycle.control_input_sequence.zeroes(horizon=STEPS))
sampled = types.bicycle.control_input_sequence.zeroes(horizon=STEPS).similar(
    array=noisy.array[:, :, 0]
)
smoothed = filters.savgol(
    window_length=WINDOW_LENGTH, polynomial_order=POLYNOMIAL_ORDER
)(optimal_input=sampled)

bicycle = model.bicycle.dynamical(time_step_size=0.1, wheelbase=2.5)
start = types.bicycle.state.create(x=0.0, y=0.0, heading=0.0, speed=5.0)
paths = {
    name: np.column_stack([states.x(), states.y()])
    for name, states in (
        ("sampled", bicycle.forward(inputs=sampled, state=start)),
        ("smoothed", bicycle.forward(inputs=smoothed, state=start)),
    )
}

asyncio.run(
    visualizer.simulation()(
        Scene(
            time_step=0.1,
            step_count=STEPS,
            at_step=lambda step: [
                render.lines(
                    name="sampled",
                    label="Sampled path",
                    strips=[paths["sampled"][: step + 2]],
                    color="#7f83f0",
                ),
                render.lines(
                    name="smoothed",
                    label="Smoothed path",
                    strips=[paths["smoothed"][: step + 2]],
                    color="#ffa487",
                ),
            ],
            plots=[
                Plot.Chart(
                    name="Steering angle",
                    plots=[
                        Plot.line(
                            name="sampled",
                            values=sampled.steering_angles(),
                            color="#7f83f0",
                        ),
                        Plot.line(
                            name="smoothed",
                            values=smoothed.steering_angles(),
                            color="#ffa487",
                        ),
                    ],
                    unit="rad",
                )
            ],
        ),
        key="savgol",
    )
)
