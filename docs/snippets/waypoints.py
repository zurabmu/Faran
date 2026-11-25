import asyncio

import numpy as np
from faran.numpy import trajectory, types
from faran_visualizer import Scene, render, visualizer

# Try moving a waypoint.
WAYPOINTS = [(0.0, 0.0), (5.0, 3.0), (10.0, 0.0), (15.0, -3.0), (20.0, 0.0)]
# Path parameters to query, as fractions of the path length.
QUERIED = np.linspace(0.0, 1.0, 9)

reference = trajectory.waypoints(points=WAYPOINTS, path_length=1.0)
curve = reference.query(
    types.path_parameters(np.linspace(0.0, 1.0, 200)[:, None])
).positions
points = reference.query(types.path_parameters(QUERIED[:, None]))
x, y, heading = points.x()[:, 0], points.y()[:, 0], points.heading()[:, 0]
tangents = [
    np.array([[x[i], y[i]], [x[i] + np.cos(heading[i]), y[i] + np.sin(heading[i])]])
    for i in range(len(x))
]

asyncio.run(
    visualizer.simulation()(
        Scene(
            time_step=0.1,
            step_count=1,
            background=[
                render.lines(
                    name="spline",
                    label="Spline",
                    strips=[curve[:, :, 0]],
                    color="#f1e4ecaa",
                ),
                render.dots(
                    name="waypoints",
                    label="Waypoints",
                    positions=np.array(WAYPOINTS),
                    color="#a3a6ff",
                    size=8.0,
                ),
                render.dots(
                    name="queried points",
                    label="Queried points",
                    positions=np.stack([x, y], axis=1),
                    color="#ffa487",
                    size=6.0,
                ),
                render.lines(
                    name="headings", label="Headings", strips=tangents, color="#ffa487"
                ),
            ],
        ),
        key="waypoints",
    )
)
