import asyncio

import numpy as np
from faran.numpy import model, types
from faran_visualizer import Plot, Scene, render, visualizer

STEERING_ANGLE = 0.3  # Radians. Try -0.3 or 0.0.
REAR_AXLE_DISTANCE = 1.0  # Meters from the reference point. Try 0.0.
STEPS = 80

bicycle = model.bicycle.dynamical(
    time_step_size=0.1,
    wheelbase=2.5,
    rear_axle_distance=REAR_AXLE_DISTANCE,
    steering_limits=(-0.5, 0.5),
)
time = np.arange(STEPS) * 0.1
inputs = types.bicycle.control_input_sequence.zeroes(horizon=STEPS).similar(
    array=np.stack(
        [np.where(time < 3.0, 1.0, 0.0), np.full(STEPS, STEERING_ANGLE)], axis=1
    )
)
states = bicycle.forward(
    inputs=inputs,
    state=types.bicycle.state.create(x=0.0, y=0.0, heading=0.0, speed=2.0),
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
                    name="vehicle",
                    label="Vehicle",
                    positions=path[step : step + 1],
                    color="#ffd2c2",
                    size=8.0,
                ),
            ],
            plots=[
                Plot.line(name="Speed", values=states.speed(), unit="m/s"),
                Plot.line(name="Heading", values=states.heading(), unit="rad"),
            ],
        ),
        key="bicycle",
    )
)
