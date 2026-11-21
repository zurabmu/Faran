from faran import trajectory
from faran_visualizer import DrivingGeometry, Poses, Road, Sizes, Types
from tests.dsl import measure

from pytest import approx, fixture, mark

import numpy as np


@fixture
def geometry() -> DrivingGeometry:
    return DrivingGeometry.create(confidence_scale=2.0)


@fixture
def sizes() -> Sizes:
    return Sizes(
        wheelbase=4.0, vehicle_width=2.0, vehicle_radius=2.0, obstacle_radius=1.5
    )


def test_that_traveled_positions_end_at_the_given_step(
    geometry: DrivingGeometry,
) -> None:
    x, y = np.array([0.0, 1.0, 2.0]), np.array([0.0, 1.0, 4.0])

    assert geometry.traveled_positions(x=x, y=y, step=0) == approx(
        np.array([[0.0, 0.0]])
    )
    assert geometry.traveled_positions(x=x, y=y, step=1) == approx(
        np.array([[0.0, 0.0], [1.0, 1.0]])
    )
    assert geometry.traveled_positions(x=x, y=y, step=2) == approx(
        np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 4.0]])
    )


def test_that_positions_on_the_reference_are_at_the_path_parameters(
    geometry: DrivingGeometry,
) -> None:
    reference = trajectory.numpy.line(start=(0.0, 0.0), end=(10.0, 0.0))

    positions = geometry.positions_on(reference, path_parameters=np.array([2.5, 7.5]))

    assert positions == approx(np.array([[2.5, 0.0], [7.5, 0.0]]))


def test_that_reference_samples_cover_the_whole_reference(
    geometry: DrivingGeometry,
) -> None:
    reference = trajectory.numpy.line(start=(0.0, 0.0), end=(10.0, 0.0))

    samples = geometry.samples_of(reference, sample_count=3)

    assert samples == approx(np.array([[0.0, 0.0], [5.0, 0.0], [10.0, 0.0]]))


@mark.parametrize("vehicle_type", ["car", "triangle"])
def test_that_a_box_vehicle_is_as_long_as_the_wheelbase_and_as_wide_as_the_vehicle(
    geometry: DrivingGeometry, sizes: Sizes, vehicle_type: Types.Vehicle
) -> None:
    shape = geometry.vehicle_shape(vehicle_type, sizes=sizes)

    (outline,) = shape.outlines(
        Poses(x=np.array([5.0]), y=np.array([5.0]), heading=np.array([0.0]))
    )

    assert measure.extent(outline) == approx((4.0, 2.0))


def test_that_a_box_vehicle_turns_with_its_heading(
    geometry: DrivingGeometry, sizes: Sizes
) -> None:
    shape = geometry.vehicle_shape("car", sizes=sizes)

    (outline,) = shape.outlines(
        Poses(x=np.array([5.0]), y=np.array([5.0]), heading=np.array([np.pi / 2]))
    )

    assert measure.extent(outline) == approx((2.0, 4.0))


def test_that_a_box_vehicle_has_no_heading_line(
    geometry: DrivingGeometry, sizes: Sizes
) -> None:
    shape = geometry.vehicle_shape("car", sizes=sizes)

    heading_lines = shape.heading_lines(
        Poses(x=np.array([5.0]), y=np.array([5.0]), heading=np.array([0.0]))
    )

    assert len(heading_lines) == 0


def test_that_a_circle_vehicle_has_its_radius(
    geometry: DrivingGeometry, sizes: Sizes
) -> None:
    shape = geometry.vehicle_shape("circle", sizes=sizes)

    (outline,) = shape.outlines(
        Poses(x=np.array([1.0]), y=np.array([1.0]), heading=np.array([0.0]))
    )

    assert measure.extent(outline) == approx((4.0, 4.0), abs=1e-2)


def test_that_the_heading_line_of_a_circle_vehicle_is_as_long_as_its_radius(
    geometry: DrivingGeometry,
    sizes: Sizes,
) -> None:
    shape = geometry.vehicle_shape("circle", sizes=sizes)

    heading_lines = shape.heading_lines(
        Poses(x=np.array([1.0]), y=np.array([1.0]), heading=np.array([np.pi / 2]))
    )

    assert heading_lines == approx(np.array([[[1.0, 1.0], [1.0, 3.0]]]))


def test_that_a_box_obstacle_has_the_size_of_the_vehicle(
    geometry: DrivingGeometry, sizes: Sizes
) -> None:
    shape = geometry.obstacle_shape("rectangle", sizes=sizes)

    (outline,) = shape.outlines(
        Poses(x=np.array([5.0]), y=np.array([5.0]), heading=np.array([0.0]))
    )

    assert measure.extent(outline) == approx((4.0, 2.0))


def test_that_a_circle_obstacle_has_the_obstacle_radius(
    geometry: DrivingGeometry, sizes: Sizes
) -> None:
    shape = geometry.obstacle_shape("circle", sizes=sizes)

    (outline,) = shape.outlines(
        Poses(x=np.array([5.0]), y=np.array([5.0]), heading=np.array([0.0]))
    )

    assert measure.extent(outline) == approx((3.0, 3.0), abs=1e-2)


def test_that_poses_without_a_finite_position_or_heading_are_left_out(
    geometry: DrivingGeometry,
) -> None:
    poses = geometry.present(
        x=np.array([5.0, np.nan, 7.0]),
        y=np.array([0.0, 1.0, 2.0]),
        heading=np.array([0.0, 0.0, np.nan]),
    )

    assert poses.x == approx(np.array([5.0]))
    assert poses.y == approx(np.array([0.0]))


def test_that_each_obstacle_has_one_forecast_path(
    geometry: DrivingGeometry,
) -> None:
    paths = geometry.forecast_paths(
        x=np.array([[5.0, 9.0], [6.0, 8.0]]), y=np.array([[0.0, 2.0], [0.0, 2.0]])
    )

    assert [path.tolist() for path in paths] == [
        [[5.0, 0.0], [6.0, 0.0]],
        [[9.0, 2.0], [8.0, 2.0]],
    ]


def test_that_forecast_points_without_a_finite_position_are_left_out(
    geometry: DrivingGeometry,
) -> None:
    paths = geometry.forecast_paths(
        x=np.array([[5.0, 9.0], [np.nan, 8.0]]), y=np.array([[0.0, 2.0], [0.0, 2.0]])
    )

    assert [path.tolist() for path in paths] == [
        [[5.0, 0.0]],
        [[9.0, 2.0], [8.0, 2.0]],
    ]


def test_that_uncertainty_ellipses_are_two_standard_deviations_wide(
    geometry: DrivingGeometry,
) -> None:
    (ellipse,) = geometry.uncertainty_ellipses(
        x=np.array([[3.0]]),
        y=np.array([[3.0]]),
        covariance=np.array([[[[4.0], [0.0]], [[0.0], [1.0]]]]),
    )

    assert measure.extent(ellipse) == approx((8.0, 4.0))


def test_that_uncertainty_ellipses_turn_with_correlated_covariances(
    geometry: DrivingGeometry,
) -> None:
    (ellipse,) = geometry.uncertainty_ellipses(
        x=np.array([[0.0]]),
        y=np.array([[0.0]]),
        covariance=np.array([[[[2.5], [1.5]], [[1.5], [2.5]]]]),
    )

    assert measure.extent_along(ellipse, direction=(1.0, 1.0)) == approx(8.0, abs=0.05)
    assert measure.extent_along(ellipse, direction=(1.0, -1.0)) == approx(4.0, abs=0.05)


def test_that_uncertainty_ellipses_use_the_first_two_state_dimensions_as_the_position(
    geometry: DrivingGeometry,
) -> None:
    (ellipse,) = geometry.uncertainty_ellipses(
        x=np.array([[3.0]]),
        y=np.array([[3.0]]),
        covariance=np.diag([4.0, 1.0, 9.0])[None, :, :, None],
    )

    assert measure.extent(ellipse) == approx((8.0, 4.0))


def test_that_covariances_that_are_not_finite_are_left_out(
    geometry: DrivingGeometry,
) -> None:
    (ellipse,) = geometry.uncertainty_ellipses(
        x=np.array([[3.0, 6.0]]),
        y=np.array([[3.0, 6.0]]),
        covariance=np.array([[[[1.0, np.nan], [0.0, 0.0]], [[0.0, 0.0], [1.0, 1.0]]]]),
    )

    assert measure.center(ellipse) == approx((3.0, 3.0))


def test_that_the_lane_surface_spans_the_lane_between_its_boundaries(
    geometry: DrivingGeometry,
) -> None:
    lane = Road.Lane(
        x=np.array([0.0, 10.0]), y=np.array([0.0, 0.0]), boundaries=(1.0, 2.0)
    )

    assert measure.extent(geometry.lane_surface(lane)) == approx((10.0, 3.0))


def test_that_marked_lane_edges_are_grouped_by_their_pattern(
    geometry: DrivingGeometry,
) -> None:
    network = Road.Network(
        lanes=[
            Road.Lane(
                x=np.array([0.0, 10.0]),
                y=np.array([0.0, 0.0]),
                boundaries=(1.0, 2.0),
                markings=("solid", "none"),
            ),
            Road.Lane(
                x=np.array([0.0, 10.0]),
                y=np.array([5.0, 5.0]),
                boundaries=(1.0, 1.0),
                markings=("dashed", "solid"),
            ),
        ]
    )

    edges = geometry.marked_edges(network)

    assert sorted(edge.tolist() for edge in edges["solid"]) == [
        [[0.0, 1.0], [10.0, 1.0]],
        [[0.0, 4.0], [10.0, 4.0]],
    ]
    assert [edge.tolist() for edge in edges["dashed"]] == [
        [[0.0, 6.0], [10.0, 6.0]],
    ]
