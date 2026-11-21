from typing import Sequence

from faran_visualizer import Plot
from tests.dsl import measure, plots

from pytest import approx, mark

import numpy as np


@mark.parametrize(
    ["lines", "values", "expected"],
    [
        (
            lines := [[1.0, 2.0], [3.0, 4.0]],
            values := [3.0, 4.0],
            expected := True,
        ),
        (lines := [[1.0, 2.0]], values := [1.0, 5.0], expected := False),
        (lines := [[1.0, 2.0]], values := [1.0, 2.0, 3.0], expected := False),
        (lines := [], values := [1.0, 2.0], expected := False),
    ],
    ids=["match among several", "different values", "different length", "no lines"],
)
def test_that_has_line_finds_a_line_only_when_one_has_the_given_values(
    lines: Sequence[Sequence[float]], values: Sequence[float], expected: bool
) -> None:
    plot = Plot(
        name="Plot",
        lines=[
            Plot.Line(label=f"Line {index}", values=np.array(it))
            for index, it in enumerate(lines)
        ],
    )

    assert plots.has_line(plot, values=values) == expected


def test_that_bound_values_returns_the_values_of_all_bounds_in_ascending_order() -> (
    None
):
    plot = Plot(
        name="Error",
        bounds=[
            Plot.Bound(label="Upper Bound", values=0.5),
            Plot.Bound(label="Lower Bound", values=-0.5),
        ],
    )

    assert plots.bound_values(plot) == approx([-0.5, 0.5])


def test_that_bound_values_includes_every_step_of_a_bound_with_values_per_step() -> (
    None
):
    plot = Plot(
        name="Progress",
        bounds=[
            Plot.Bound(label="Path Length", values=np.array([3.0, 1.0])),
            Plot.Bound(label="Limit", values=2.0),
        ],
    )

    assert plots.bound_values(plot) == approx([1.0, 2.0, 3.0])


def test_that_bound_values_returns_no_values_for_a_plot_without_bounds() -> None:
    plot = Plot(name="Speed")

    assert len(plots.bound_values(plot)) == 0


def test_that_measure_extent_returns_the_width_and_height_of_a_strip() -> None:
    strip = [[1.0, 1.0], [4.0, 3.0], [2.0, 5.0]]

    assert measure.extent(strip) == approx((3.0, 4.0))


def test_that_measure_extent_along_measures_a_strip_along_the_direction() -> None:
    square = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]

    assert measure.extent_along(square, direction=(1.0, 1.0)) == approx(np.sqrt(2.0))


def test_that_measure_extent_along_does_not_depend_on_the_length_of_the_direction() -> (
    None
):
    strip = [[0.0, 0.0], [3.0, 4.0]]

    assert measure.extent_along(strip, direction=(6.0, 8.0)) == approx(
        measure.extent_along(strip, direction=(0.6, 0.8))
    )


def test_that_measure_center_returns_the_center_of_the_box_around_a_strip() -> None:
    strip = [[1.0, 1.0], [4.0, 3.0], [2.0, 5.0]]

    assert measure.center(strip) == approx((2.5, 3.0))
