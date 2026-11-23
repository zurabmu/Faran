from dataclasses import replace
from pathlib import Path

from faran_visualizer import (
    Info,
    InconsistentRenderingsError,
    InvalidColorError,
    Plot,
    RerunRenderer,
    Scene,
    Theme,
    configure,
    render,
    visualizer,
)
from tests.dsl import Visualize, files

from pytest import approx, mark, raises

import numpy as np


async def test_that_the_visualization_is_saved_at_the_correct_path(
    tmp_path: Path,
) -> None:
    visualize = visualizer.simulation(
        output="results", output_directory=tmp_path, renderer=RerunRenderer()
    )

    await visualize(Scene(time_step=0.1, step_count=1), key="run")

    assert files.in_directory(tmp_path / "results") == ["run.frn"]


@mark.parametrize(
    ["candidate", "can_visualize"],
    [
        (candidate := Scene(time_step=0.1, step_count=1), can_visualize := True),
        (
            candidate := render.dots(
                name="dot", label="dot", positions=np.array([[0.0, 0.0]]), color="red"
            ),
            can_visualize := False,
        ),
        (candidate := "not a scene", can_visualize := False),
        (candidate := None, can_visualize := False),
    ],
    ids=["scene", "rendering alone", "string", "nothing"],
)
async def test_that_only_scenes_can_be_visualized(
    candidate: object, can_visualize: bool
) -> None:
    assert await visualizer.simulation().can_visualize(candidate) == can_visualize


async def test_that_the_renderings_of_each_step_are_shown(
    visualize: Visualize,
) -> None:
    positions = np.array([[0.0, 0.0], [1.0, 1.0], [2.0, 4.0]])
    scene = Scene(
        time_step=0.1,
        step_count=3,
        at_step=lambda step: [
            render.lines(
                name="path", label="path", strips=[positions[: step + 1]], color="red"
            ),
            render.dots(
                name="robot",
                label="robot",
                positions=positions[step : step + 1],
                color="red",
            ),
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.lines(at="path", step=0) == [[[0.0, 0.0]]]
    assert visualization.lines(at="path", step=1) == [[[0.0, 0.0], [1.0, 1.0]]]
    assert visualization.lines(at="path", step=2) == [
        [[0.0, 0.0], [1.0, 1.0], [2.0, 4.0]]
    ]

    assert visualization.dots(at="robot", step=0) == [[0.0, 0.0]]
    assert visualization.dots(at="robot", step=1) == [[1.0, 1.0]]
    assert visualization.dots(at="robot", step=2) == [[2.0, 4.0]]


async def test_that_the_background_is_shown_at_every_step(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=3,
        background=[
            render.lines(
                name="reference",
                label="reference",
                strips=[np.array([[0.0, 0.0], [10.0, 0.0]])],
                color="gray",
            )
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.lines(at="reference", step=0) == [[[0.0, 0.0], [10.0, 0.0]]]
    assert visualization.lines(at="reference", step=1) == [[[0.0, 0.0], [10.0, 0.0]]]
    assert visualization.lines(at="reference", step=2) == [[[0.0, 0.0], [10.0, 0.0]]]


async def test_that_renderings_that_change_between_steps_are_rejected(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=2,
        at_step=lambda step: [
            render.dots(
                name=f"robot {step}",
                label=f"robot {step}",
                positions=np.array([[0.0, 0.0]]),
                color="red",
            )
        ],
    )

    with raises(InconsistentRenderingsError):
        await visualize.scene(scene)


async def test_that_the_values_of_a_plot_are_rendered_at_each_step(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=3,
        plots=[Plot.line(name="Speed", values=np.array([1.0, 2.0, 3.0]))],
    )

    visualization = await visualize.scene(scene)

    assert visualization.plot_line(at="Speed") == approx([1.0, 2.0, 3.0])


async def test_that_a_constant_bound_of_a_plot_is_rendered_at_every_step(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=3,
        plots=[
            Plot.line(
                name="Speed",
                values=np.array([1.0, 2.0, 3.0]),
                bounds=[Plot.Bound(label="Limit", values=2.5)],
            )
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.plot_line(at="Limit") == approx([2.5, 2.5, 2.5])


async def test_that_the_upper_and_lower_bounds_of_a_band_are_rendered(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=2,
        plots=[
            Plot(
                name="Risk",
                bands=[
                    Plot.Band(
                        label="Spread",
                        lower_label="Minimum",
                        upper_label="Maximum",
                        lower=np.array([1.0, 2.0]),
                        upper=np.array([3.0, 4.0]),
                    )
                ],
            )
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.plot_line(at="Minimum") == approx([1.0, 2.0])
    assert visualization.plot_line(at="Maximum") == approx([3.0, 4.0])


async def test_that_the_lines_of_several_bands_have_different_names_by_default(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=2,
        plots=[
            Plot(
                name="Risk",
                bands=[
                    Plot.Band(
                        label="Inner",
                        lower=np.array([1.0, 2.0]),
                        upper=np.array([3.0, 4.0]),
                    ),
                    Plot.Band(
                        label="Outer",
                        lower=np.array([0.0, 1.0]),
                        upper=np.array([5.0, 6.0]),
                    ),
                ],
            )
        ],
    )

    visualization = await visualize.scene(scene)

    names = visualization.plot_line_names()
    assert len(set(names)) == 4
    assert sorted(visualization.plot_line(at=name) for name in names) == [
        [0.0, 1.0],
        [1.0, 2.0],
        [3.0, 4.0],
        [5.0, 6.0],
    ]


async def test_that_the_plots_of_a_plot_chart_are_rendered_together(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=1,
        plots=[
            Plot.Chart(
                name="Errors",
                plots=[
                    Plot.line(name="Contouring", values=np.array([0.1])),
                    Plot.line(name="Lag", values=np.array([0.2])),
                ],
            ),
            Plot.line(name="Speed", values=np.array([1.0])),
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.plot_of(at="Contouring") == visualization.plot_of(at="Lag")
    assert visualization.plot_of(at="Speed") != visualization.plot_of(at="Contouring")


@mark.parametrize("color", ["blue", "Blue", "#00f", "#0000ff", "#0000FF", "#0000ff80"])
async def test_that_supported_colors_are_accepted(
    visualize: Visualize, color: str
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=1,
        at_step=lambda step: [
            render.dots(
                name="robot",
                label="robot",
                positions=np.array([[0.0, 0.0]]),
                color=color,
            )
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.dots(at="robot", step=0) == [[0.0, 0.0]]


@mark.parametrize("color", ["sky", "0000ff", "#00ff", "#0000fg", "#", ""])
async def test_that_colors_that_are_not_supported_are_rejected(
    visualize: Visualize, color: str
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=1,
        at_step=lambda step: [
            render.dots(
                name="robot",
                label="robot",
                positions=np.array([[0.0, 0.0]]),
                color=color,
            )
        ],
    )

    with raises(InvalidColorError):
        await visualize.scene(scene)


async def test_that_the_info_value_of_each_step_is_shown(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=3,
        info=[Info(label="Altitude", values=np.array([1.0, 2.0, 3.0]), unit="m")],
    )

    visualization = await visualize.scene(scene)

    assert visualization.info(at="Altitude", step=0) == approx(1.0)
    assert visualization.info(at="Altitude", step=1) == approx(2.0)
    assert visualization.info(at="Altitude", step=2) == approx(3.0)


def test_that_a_visualizer_uses_the_globally_configured_theme_when_none_is_given(
    tmp_path: Path,
) -> None:
    theme = replace(Theme.default(), background="#20192b")
    configure(output_directory=tmp_path, theme=theme)

    try:
        assert visualizer.simulation().theme == theme
        assert visualizer.mpcc().inner.theme == theme
    finally:
        configure(output_directory=tmp_path)


async def test_that_renderings_with_the_same_label_share_one_legend_entry(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=1,
        at_step=lambda step: [
            render.lines(
                name="obstacles/bodies",
                label="Obstacles",
                strips=[np.array([[0.0, 0.0], [1.0, 0.0]])],
                color="red",
            ),
            render.lines(
                name="obstacles/headings",
                label="Obstacles",
                strips=[np.array([[0.0, 0.0], [0.5, 0.0]])],
                color="red",
            ),
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.legend() == ["Obstacles"]


async def test_that_the_legend_lists_labels_in_the_order_they_first_appear(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=1,
        background=[
            render.lines(
                name="reference",
                label="Reference path",
                strips=[np.array([[0.0, 0.0], [10.0, 0.0]])],
                color="gray",
            )
        ],
        at_step=lambda step: [
            render.lines(
                name="plan",
                label="Plan",
                strips=[np.array([[0.0, 0.0], [1.0, 0.0]])],
                color="blue",
            ),
            render.dots(
                name="robot",
                label="Robot",
                positions=np.array([[0.0, 0.0]]),
                color="red",
            ),
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.legend() == ["Reference path", "Plan", "Robot"]


async def test_that_a_legend_sample_shows_the_first_line_and_dot_of_its_label(
    visualize: Visualize,
) -> None:
    scene = Scene(
        time_step=0.1,
        step_count=1,
        at_step=lambda step: [
            render.dots(
                name="plan/points",
                label="Plan",
                positions=np.array([[0.0, 0.0]]),
                color="#00ff00",
            ),
            render.lines(
                name="plan",
                label="Plan",
                strips=[np.array([[0.0, 0.0], [1.0, 0.0]])],
                color="#0000ff",
                pattern="dashed",
            ),
            render.lines(
                name="plan/outline",
                label="Plan",
                strips=[np.array([[0.0, 0.0], [1.0, 0.0]])],
                color="#ff0000",
            ),
        ],
    )

    visualization = await visualize.scene(scene)

    assert visualization.legend_sample(at="Plan") == [
        "dashed line #0000ffff",
        "dot #00ff00ff",
    ]
