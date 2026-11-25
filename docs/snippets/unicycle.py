import asyncio

import numpy as np
from faran.numpy import model, types
from faran_visualizer import Plot, Scene, render, visualizer

ANGULAR_VELOCITY = 0.5  # Radians per second. Try -0.5 or 1.5.
STEPS = 100

unicycle = model.unicycle.dynamical(
    time_step_size=0.1, speed_limits=(-5.0, 5.0), angular_velocity_limits=(-1.0, 1.0)
)
time = np.arange(STEPS) * 0.1
inputs = types.unicycle.control_input_sequence.zeroes(horizon=STEPS).similar(
    array=np.stack(
        [np.full(STEPS, 2.0), ANGULAR_VELOCITY * np.sign(np.sin(time))], axis=1
    )
)
states = unicycle.forward(
    inputs=inputs, state=types.unicycle.state.create(x=0.0, y=0.0, heading=0.0)
)
path = np.column_stack([states.x(), states.y()])

asyncio.run(
    visualizer.simulation()(
        Scene(
            time_step=0.1,
            step_count=STEPS,
            at_step=lambda step: [
                render.lines(
                    name="path",
                    label="Traveled path",
                    strips=[path[: step + 2]],
                    color="#ffa487",
                ),
                render.dots(
                    name="robot",
                    label="Robot",
                    positions=path[step : step + 1],
                    color="#ffd2c2",
                    size=8.0,
                ),
            ],
            plots=[Plot.line(name="Heading", values=states.heading(), unit="rad")],
        ),
        key="unicycle",
    )
)
