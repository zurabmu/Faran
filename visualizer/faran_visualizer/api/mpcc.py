from typing import Callable, Sequence, Protocol
from dataclasses import dataclass, field

from faran import (
    Trajectory,
    ExplicitBoundary,
    BoundaryPoints,
    ReferencePoints,
    ControlInputSequence,
    Weights,
    Control,
    Risk,
    types,
)

from faran_visualizer.api.config import OutputPath
from faran_visualizer.api.simulation import SimulationVisualizer
from faran_visualizer.array import Array, JaxArray
from faran_visualizer.driving import (
    DrivingGeometry,
    Poses,
    Sizes,
    Strips,
    Styles,
    boundaries,
    ego_body,
    ego_info,
    forecasts,
    ghost,
    nominal_plan,
    obstacle_bodies,
    observations,
    optimal_plan,
    points_from,
    reference,
    road,
    traveled_path,
    uncertainties,
)
from faran_visualizer.data import Plot, Plots, Road, Types
from faran_visualizer.scene import Renderer, Rendering, Points, Scene
from faran_visualizer.theme import Theme

from jaxtyping import Float

import numpy as np

type PhysicalStateSequence = (
    types.numpy.bicycle.StateSequence | types.jax.bicycle.StateSequence
)
type VirtualStateSequence = (
    types.numpy.simple.StateSequence | types.jax.simple.StateSequence
)
type AugmentedStateSequence = types.augmented.State[
    PhysicalStateSequence, VirtualStateSequence
]
type PathParameters = types.numpy.PathParameters
type ObstacleStateValues = Float[Array, "T K"] | Float[JaxArray, "T K"]
type ObstacleCovariances = Float[Array, "T D_x D_x K"] | Float[JaxArray, "T D_x D_x K"]
type TrackingErrors = Float[Array, " T"] | Float[JaxArray, " T"]


class ObstacleStates(Protocol):
    def x(self) -> ObstacleStateValues:
        """Returns the x-coordinates of the obstacles."""
        ...

    def y(self) -> ObstacleStateValues:
        """Returns the y-coordinates of the obstacles."""
        ...

    def heading(self) -> ObstacleStateValues:
        """Returns the headings of the obstacles."""
        ...

    def covariance(
        self,
    ) -> ObstacleCovariances | None:
        """Returns the covariances of the obstacle states, or None if not available."""
        ...


@dataclass(kw_only=True, frozen=True)
class MpccSimulationResult:
    """Data for one simulation where an MPCC problem formulation was used for
    the trajectory planning of an automated driving vehicle.

    Attributes:
        reference: The reference path the ego follows.
        states: The ego states. The first virtual state must be the path parameter.
        contouring_errors: The contouring error at each step, in meters.
        lag_errors: The lag error at each step, in meters.
        time_step_size: The time between two steps, in seconds.
        wheelbase: The length of the boxes rendered for the ego and obstacles, in
            meters. Required when either is rendered as a box.
        vehicle_width: The width of the boxes rendered for the ego and obstacles, in
            meters. Required when either is rendered as a box.
        max_contouring_error: Rendered as upper and lower bounds on the contouring
            error plot.
        max_lag_error: Rendered as upper and lower bounds on the lag error plot.
        vehicle_type: `"car"` and `"triangle"` render the ego as a box, `"circle"` as
            a circle.
        obstacle_shape: `"rectangle"` renders obstacles as boxes, `"circle"` as
            circles.
        vehicle_radius: The radius of the ego, in meters. Required when
            `vehicle_type` is `"circle"`.
        obstacle_radius: The radius of the obstacles, in meters. Required when
            `obstacle_shape` is `"circle"`.
        optimal_trajectories: The optimal plan of each step.
        nominal_trajectories: The nominal plan of each step. Rendered only together
            with `optimal_trajectories`.
        obstacles: The obstacle states at each step.
        obstacle_observations: The observed obstacle states at each step. Rendered
            only together with `obstacles`.
        obstacle_forecasts: The forecast of the obstacle states at each step. Rendered
            only together with `obstacles`. The first two state dimensions of a
            covariance must be x and y.
        controls: The control of each step. Its rollout weights are used for the
            risk plot.
        risks: The risk of each rollout at each step. The risk plot is rendered only
            when both `risks` and `controls` are given.
        network: The lanes to render.
        boundary: The corridor boundary to render.
    """

    reference: Trajectory[PathParameters, ReferencePoints]
    states: AugmentedStateSequence
    contouring_errors: TrackingErrors
    lag_errors: TrackingErrors
    time_step_size: float
    wheelbase: float | None = None
    vehicle_width: float | None = None
    max_contouring_error: float | None = None
    max_lag_error: float | None = None
    vehicle_type: Types.Vehicle = "car"
    obstacle_shape: Types.ObstacleShape = "rectangle"
    vehicle_radius: float | None = None
    obstacle_radius: float | None = None
    optimal_trajectories: Sequence[AugmentedStateSequence] | None = None
    nominal_trajectories: Sequence[AugmentedStateSequence] | None = None
    obstacles: ObstacleStates | None = None
    obstacle_observations: ObstacleStates | None = None
    obstacle_forecasts: Sequence[ObstacleStates] | None = None
    controls: Sequence[Control[ControlInputSequence, Weights]] | None = None
    risks: Sequence[Risk] | None = None
    network: Road.Network | None = None
    boundary: ExplicitBoundary | None = None


@dataclass(kw_only=True, frozen=True)
class MpccPlots:
    """The plots `MpccVisualizer` creates for one simulation result.

    Attributes:
        progress: The path parameter, with the path length as a bound.
        tracking_errors: The chart of the contouring and lag errors.
        contouring_error: The contouring error, bounded by its maximum if given.
        lag_error: The lag error, bounded by its maximum if given.
        risk: The risk of the selected and median rollouts, or None without risks
            and controls.
    """

    progress: Plot
    tracking_errors: Plot.Chart
    contouring_error: Plot
    lag_error: Plot
    risk: Plot | None

    @property
    def all(self) -> list[Plot | Plot.Chart]:
        """The plots in the order `MpccVisualizer` shows them by default."""
        return [
            self.progress,
            self.tracking_errors,
            *([self.risk] if self.risk is not None else []),
        ]


class PlotSelection(Protocol):
    def __call__(self, plots: MpccPlots, result: MpccSimulationResult, /) -> Plots:
        """Returns the plots to show for `result`, given the `plots` that
        `MpccVisualizer` creates for it. Return other plots to override them, or
        add to `MpccPlots.all` to extend them.

        Example:
            Show the speed of the ego after the default plots:

            ```python
            MpccVisualizer.create(
                plots=lambda plots, result: [
                    *plots.all,  # show the default plots first
                    Plot.line(
                        name="Speed",
                        values=np.asarray(result.states.physical.speed()),
                        unit="m/s",
                    ),
                ]
            )
            ```
        """
        ...


type FramePart = Callable[[int], list[Rendering]]
"""Returns the renderings of one part of the scene at a step."""


def _all_plots(plots: MpccPlots, result: MpccSimulationResult) -> Plots:
    return plots.all


@dataclass(kw_only=True, frozen=True)
class MpccVisualizer:
    """Visualizer for MPCC simulation results.

    Attributes:
        inner: The visualizer that saves the converted simulation result.
        reference_sample_count: The number of points rendered along the reference path.
        boundary_sample_count: The number of points rendered along each corridor
            boundary.
        styles: How each part of the scene is drawn.
        plots: Chooses the plots to show for each simulation result.
        geometry: Computes the positions and outlines that are rendered.
    """

    inner: SimulationVisualizer
    reference_sample_count: int
    boundary_sample_count: int
    styles: Styles
    plots: PlotSelection = _all_plots
    geometry: DrivingGeometry = field(default_factory=DrivingGeometry.create)

    @staticmethod
    def create(
        *,
        output: str = "mpcc-simulation",
        reference_sample_count: int = 200,
        boundary_sample_count: int = 100,
        output_directory: OutputPath | None = None,
        plots: PlotSelection = _all_plots,
        theme: Theme | None = None,
        renderer: Renderer | None = None,
    ) -> "MpccVisualizer":
        """Creates a visualizer that saves visualizations in
        `<output_directory>/<output>`, in the colors of `theme`, with `renderer`.
        Omitted configuration values are taken from the global configuration."""
        inner = SimulationVisualizer.create(
            output=output,
            output_directory=output_directory,
            theme=theme,
            renderer=renderer,
        )
        return MpccVisualizer(
            inner=inner,
            reference_sample_count=reference_sample_count,
            boundary_sample_count=boundary_sample_count,
            styles=Styles.of(inner.theme),
            plots=plots,
        )

    async def __call__(self, data: MpccSimulationResult, *, key: str) -> None:
        """Saves the simulation as a visualization at `<output>/<key>` with the
        extension of the renderer."""
        await self.inner(self.scene_of(data), key=key)

    async def can_visualize(self, data: object) -> bool:
        return isinstance(data, MpccSimulationResult)

    def scene_of(self, result: MpccSimulationResult) -> Scene:
        """Converts the simulation result into the scene `SimulationVisualizer`
        shows."""
        path_parameters = self._path_parameters_from(result)
        parts = [
            self._ego_path_part(result),
            *self._plan_parts(result),
            *self._obstacle_parts(result),
            self._ghost_part(result, path_parameters=path_parameters),
            self._ego_body_part(result),
        ]
        return Scene(
            time_step=result.time_step_size,
            step_count=len(path_parameters),
            background=self._background_from(result),
            at_step=lambda step: [
                rendering for part in parts for rendering in part(step)
            ],
            plots=self.plots(self.plots_from(result), result),
            info=ego_info(
                time_step=result.time_step_size,
                x=np.asarray(result.states.physical.x()),
                y=np.asarray(result.states.physical.y()),
                heading=np.asarray(result.states.physical.heading()),
                path_parameters=path_parameters,
                path_length=result.reference.path_length,
            ),
        )

    def plots_from(self, result: MpccSimulationResult) -> MpccPlots:
        """Returns the plots `MpccVisualizer` creates for the simulation result."""
        return MpccPlots(
            progress=Plot(
                name="Path Progress",
                unit="m",
                lines=[
                    Plot.Line(
                        label="Progress", values=self._path_parameters_from(result)
                    )
                ],
                bounds=[
                    Plot.Bound(label="Path Length", values=result.reference.path_length)
                ],
            ),
            tracking_errors=Plot.Chart(
                name="Tracking Errors",
                unit="m",
                plots=[
                    contouring_error := Plot(
                        name="Contouring Error",
                        lines=[
                            Plot.Line(
                                label="Contouring Error",
                                values=np.asarray(result.contouring_errors).flatten(),
                            )
                        ],
                        bounds=_symmetric_bounds(result.max_contouring_error),
                    ),
                    lag_error := Plot(
                        name="Lag Error",
                        lines=[
                            Plot.Line(
                                label="Lag Error",
                                values=np.asarray(result.lag_errors).flatten(),
                            )
                        ],
                        bounds=_symmetric_bounds(result.max_lag_error),
                    ),
                ],
            ),
            contouring_error=contouring_error,
            lag_error=lag_error,
            risk=self._risk_plot_from(result),
        )

    def _background_from(self, result: MpccSimulationResult) -> list[Rendering]:
        return [
            *self._road_from(result),
            reference(
                self.geometry.samples_of(
                    result.reference, sample_count=self.reference_sample_count
                ),
                styles=self.styles,
            ),
            *self._boundaries_from(result),
        ]

    def _road_from(self, result: MpccSimulationResult) -> list[Rendering]:
        if (network := result.network) is None:
            return []

        return road(
            surfaces=[self.geometry.lane_surface(lane) for lane in network.lanes],
            edges_by_pattern=self.geometry.marked_edges(network),
            styles=self.styles,
        )

    def _boundaries_from(self, result: MpccSimulationResult) -> list[Rendering]:
        if (boundary := result.boundary) is None:
            return []

        return [
            boundaries(
                left=_positions_in(
                    boundary.left(sample_count=self.boundary_sample_count)
                ),
                right=_positions_in(
                    boundary.right(sample_count=self.boundary_sample_count)
                ),
                styles=self.styles,
            )
        ]

    def _ego_path_part(self, result: MpccSimulationResult) -> FramePart:
        x = np.asarray(result.states.physical.x())
        y = np.asarray(result.states.physical.y())
        return lambda step: [
            traveled_path(
                self.geometry.traveled_positions(x=x, y=y, step=step),
                styles=self.styles,
            )
        ]

    def _ego_body_part(self, result: MpccSimulationResult) -> FramePart:
        x = np.asarray(result.states.physical.x())
        y = np.asarray(result.states.physical.y())
        heading = np.asarray(result.states.physical.heading())
        shape = self.geometry.vehicle_shape(
            result.vehicle_type, sizes=_sizes_of(result)
        )
        return lambda step: ego_body(
            Poses(
                x=x[step : step + 1],
                y=y[step : step + 1],
                heading=heading[step : step + 1],
            ),
            shape=shape,
            styles=self.styles,
        )

    def _ghost_part(
        self, result: MpccSimulationResult, *, path_parameters: Float[Array, " T"]
    ) -> FramePart:
        positions = self.geometry.positions_on(
            result.reference, path_parameters=path_parameters
        )
        return lambda step: [ghost(positions[step : step + 1], styles=self.styles)]

    def _path_parameters_from(self, result: MpccSimulationResult) -> Float[Array, " T"]:
        # NOTE: We assume the first virtual dimension is the path parameter.
        return np.asarray(result.states.virtual)[:, 0]

    def _plan_parts(self, result: MpccSimulationResult) -> list[FramePart]:
        if (optimal := result.optimal_trajectories) is None:
            return []

        return [
            lambda step: optimal_plan(_positions_of(optimal[step]), styles=self.styles),
            *self._nominal_plan_parts(result),
        ]

    def _nominal_plan_parts(self, result: MpccSimulationResult) -> list[FramePart]:
        if (nominal := result.nominal_trajectories) is None:
            return []

        return [
            lambda step: nominal_plan(_positions_of(nominal[step]), styles=self.styles)
        ]

    def _obstacle_parts(self, result: MpccSimulationResult) -> list[FramePart]:
        if (obstacles := result.obstacles) is None:
            return []

        shape = self.geometry.obstacle_shape(
            result.obstacle_shape, sizes=_sizes_of(result)
        )
        return [
            *self._forecast_parts(result),
            lambda step: obstacle_bodies(
                self._present_at(obstacles, step=step), shape=shape, styles=self.styles
            ),
            *self._observation_parts(result),
        ]

    def _forecast_parts(self, result: MpccSimulationResult) -> list[FramePart]:
        if (predicted := result.obstacle_forecasts) is None:
            return []

        return [
            lambda step: [
                uncertainties(self._ellipses_of(predicted[step]), styles=self.styles)
            ],
            lambda step: forecasts(
                self.geometry.forecast_paths(
                    x=np.asarray(predicted[step].x()),
                    y=np.asarray(predicted[step].y()),
                ),
                styles=self.styles,
            ),
        ]

    def _observation_parts(self, result: MpccSimulationResult) -> list[FramePart]:
        if (observed := result.obstacle_observations) is None:
            return []

        return [
            lambda step: observations(
                self._present_at(observed, step=step), styles=self.styles
            )
        ]

    def _present_at(self, obstacles: ObstacleStates, *, step: int) -> Poses:
        return self.geometry.present(
            x=np.asarray(obstacles.x())[step],
            y=np.asarray(obstacles.y())[step],
            heading=np.asarray(obstacles.heading())[step],
        )

    def _ellipses_of(self, forecast: ObstacleStates) -> Strips:
        if (covariance := forecast.covariance()) is None:
            return np.empty((0, 0, 2))

        return self.geometry.uncertainty_ellipses(
            x=np.asarray(forecast.x()),
            y=np.asarray(forecast.y()),
            covariance=np.asarray(covariance),
        )

    def _risk_plot_from(self, result: MpccSimulationResult) -> Plot | None:
        if (
            result.risks is None
            or result.controls is None
            or len(result.risks) == 0
            or len(result.controls) == 0
        ):
            return None

        risks = np.stack([np.asarray(risk) for risk in result.risks], axis=0).sum(
            axis=1
        )
        weights = np.stack(
            [
                np.asarray(control.debug.trajectory_weights)
                for control in result.controls
            ],
            axis=0,
        )

        # NOTE: avoid zero risks for log scale plotting
        risks = np.maximum(risks, 1e-10)
        selected = (risks * weights).sum(axis=1)

        return Plot(
            name="Risk",
            scale="log",
            lines=[
                Plot.Line(label="Selected", values=selected),
                Plot.Line(label="Median", values=np.median(risks, axis=1)),
            ],
            bands=[
                Plot.Band(
                    label="10-90%",
                    lower=np.percentile(risks, 10, axis=1),
                    upper=np.percentile(risks, 90, axis=1),
                ),
                Plot.Band(
                    label="25-75%",
                    lower=np.percentile(risks, 25, axis=1),
                    upper=np.percentile(risks, 75, axis=1),
                ),
            ],
        )


def _symmetric_bounds(maximum: float | None) -> list[Plot.Bound]:
    if maximum is None:
        return []

    return [
        Plot.Bound(label="Upper Bound", values=maximum),
        Plot.Bound(label="Lower Bound", values=-maximum),
    ]


def _sizes_of(result: MpccSimulationResult) -> Sizes:
    return Sizes(
        wheelbase=result.wheelbase,
        vehicle_width=result.vehicle_width,
        vehicle_radius=result.vehicle_radius,
        obstacle_radius=result.obstacle_radius,
    )


def _positions_of(trajectory: AugmentedStateSequence) -> Points:
    return points_from(
        np.asarray(trajectory.physical.x()), np.asarray(trajectory.physical.y())
    )


def _positions_in(points: BoundaryPoints) -> Points:
    return np.asarray(points)[:, :2]
