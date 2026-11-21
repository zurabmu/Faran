from typing import Callable, Sequence

from faran_visualizer import (
    MpccPlots,
    MpccSimulationResult,
    MpccVisualizer,
    Plot,
    Plots,
)
from tests.dsl import MpccData, plots

from pytest import approx, mark

import numpy as np


def test_that_progress_is_plotted_with_the_path_length_as_upper_bound(
    mpcc: MpccData,
) -> None:
    result = mpcc.result(
        states=mpcc.states(x=[0.0, 1.0], path_parameters=[2.0, 4.0]), path_length=20.0
    )
    mpcc_visualizer = MpccVisualizer.create()

    progress = mpcc_visualizer.plots_from(result).progress

    (line,) = progress.lines
    (bound,) = progress.bounds
    assert line.values == approx(np.array([2.0, 4.0]))
    assert bound.values == approx(20.0)


@mark.parametrize(
    ["max_contouring_error", "max_lag_error", "error_plot"],
    [
        (
            max_contouring_error := 0.5,
            max_lag_error := None,
            error_plot := lambda plots: plots.contouring_error,
        ),
        (
            max_contouring_error := None,
            max_lag_error := 0.5,
            error_plot := lambda plots: plots.lag_error,
        ),
    ],
    ids=["contouring error", "lag error"],
)
def test_that_the_maximum_error_is_plotted_as_upper_and_lower_bounds(
    mpcc: MpccData,
    max_contouring_error: float | None,
    max_lag_error: float | None,
    error_plot: Callable[[MpccPlots], Plot],
) -> None:
    result = mpcc.result(
        max_contouring_error=max_contouring_error, max_lag_error=max_lag_error
    )
    mpcc_visualizer = MpccVisualizer.create()

    error = error_plot(mpcc_visualizer.plots_from(result))

    assert plots.bound_values(error) == approx([-0.5, 0.5])


@mark.parametrize(
    "error_plot",
    [lambda plots: plots.contouring_error, lambda plots: plots.lag_error],
    ids=["contouring error", "lag error"],
)
def test_that_errors_have_no_bounds_without_a_maximum_error(
    mpcc: MpccData, error_plot: Callable[[MpccPlots], Plot]
) -> None:
    mpcc_visualizer = MpccVisualizer.create()

    error = error_plot(mpcc_visualizer.plots_from(mpcc.result()))

    assert len(error.bounds) == 0


def test_that_the_tracking_errors_are_plotted_at_each_step(
    mpcc: MpccData,
) -> None:
    result = mpcc.result(contouring_errors=[0.1, -0.2], lag_errors=[0.3, 0.4])
    mpcc_visualizer = MpccVisualizer.create()

    plots = mpcc_visualizer.plots_from(result)

    (contouring,) = plots.contouring_error.lines
    (lag,) = plots.lag_error.lines
    assert contouring.values == approx(np.array([0.1, -0.2]))
    assert lag.values == approx(np.array([0.3, 0.4]))


def test_that_the_weighted_and_median_risk_of_the_rollouts_are_plotted(
    mpcc: MpccData,
) -> None:
    result = mpcc.result(
        risks=[
            mpcc.risk([[1.0, 2.0, 6.0], [1.0, 2.0, 6.0]]),
            mpcc.risk([[0.5, 1.0, 1.5], [0.5, 1.0, 1.5]]),
        ],
        controls=[
            mpcc.control(weights=[0.5, 0.5, 0.0]),
            mpcc.control(weights=[0.0, 0.0, 1.0]),
        ],
    )
    mpcc_visualizer = MpccVisualizer.create()

    risk = mpcc_visualizer.plots_from(result).risk

    assert risk is not None

    assert plots.has_line(risk, values=[3.0, 3.0])
    assert plots.has_line(risk, values=[4.0, 2.0])


def test_that_zero_risk_is_plotted_as_a_small_positive_value(
    mpcc: MpccData,
) -> None:
    result = mpcc.result(
        risks=[mpcc.risk([[0.0, 0.0]]), mpcc.risk([[0.0, 0.0]])],
        controls=[mpcc.control(weights=[0.5, 0.5])] * 2,
    )
    mpcc_visualizer = MpccVisualizer.create()

    risk = mpcc_visualizer.plots_from(result).risk

    assert risk is not None

    assert all(np.all(line.values > 0.0) for line in risk.lines)
    assert all(np.all(band.lower > 0.0) for band in risk.bands)


@mark.parametrize(
    ["risks", "weights"],
    [
        (risks := None, weights := None),
        (risks := [[[1.0]], [[1.0]]], weights := None),
        (risks := None, weights := [[1.0], [1.0]]),
        (risks := [], weights := []),
    ],
    ids=["neither", "only risks", "only controls", "empty"],
)
def test_that_risk_is_not_plotted_without_both_risks_and_controls(
    mpcc: MpccData,
    risks: Sequence[Sequence[Sequence[float]]] | None,
    weights: Sequence[Sequence[float]] | None,
) -> None:
    result = mpcc.result(
        risks=None if risks is None else [mpcc.risk(it) for it in risks],
        controls=None
        if weights is None
        else [mpcc.control(weights=it) for it in weights],
    )
    mpcc_visualizer = MpccVisualizer.create()

    assert mpcc_visualizer.plots_from(result).risk is None


def test_that_only_the_selected_plots_are_shown(
    mpcc: MpccData,
) -> None:
    speed = Plot.line(name="Speed", values=np.array([1.0, 2.0]))
    mpcc_visualizer = MpccVisualizer.create(plots=lambda plots, result: [speed])

    scene = mpcc_visualizer.scene_of(mpcc.result())

    assert scene.plots == [speed]


def test_that_extra_plots_are_shown_after_the_default_plots(
    mpcc: MpccData,
) -> None:
    speed = Plot.line(name="Speed", values=np.array([1.0, 2.0]))
    mpcc_visualizer = MpccVisualizer.create(
        plots=lambda plots, result: [*plots.all, speed]
    )

    scene = mpcc_visualizer.scene_of(mpcc.result())

    assert scene.plots[-1] is speed
    assert len(scene.plots) > 1


def test_that_the_plot_selection_receives_the_simulation_result(
    mpcc: MpccData,
) -> None:
    received: list[MpccSimulationResult] = []

    def select(plots: MpccPlots, result: MpccSimulationResult) -> Plots:
        received.append(result)
        return plots.all

    result = mpcc.result()
    MpccVisualizer.create(plots=select).scene_of(result)

    (received_result,) = received
    assert received_result is result
