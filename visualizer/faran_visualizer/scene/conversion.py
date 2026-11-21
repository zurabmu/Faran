from typing import Sequence

from faran_visualizer.data import plots_in
from faran_visualizer.scene.charts import charts_from
from faran_visualizer.scene.description import Scene
from faran_visualizer.scene.info import rows_at
from faran_visualizer.scene.animation import Animation, Rendering, Frame


class InconsistentRenderingsError(ValueError):
    """Raised when the steps of a scene render differently named renderings."""


def animation_from(scene: Scene) -> Animation:
    """Renders every step of the scene and resolves its plots and info table.

    Raises:
        InconsistentRenderingsError: If a step renders renderings with other names, or in
            another order, than the first step.
    """
    check_step_counts(scene)
    frames = [frame_at(scene, step=step) for step in range(scene.step_count)]
    check_names(frames)
    return Animation(
        time_step=scene.time_step,
        background=scene.background,
        frames=frames,
        charts=charts_from(scene.plots, step_count=scene.step_count),
    )


def frame_at(scene: Scene, *, step: int) -> Frame:
    return Frame(renderings=scene.at_step(step), info=rows_at(scene.info, step=step))


def check_step_counts(scene: Scene) -> None:
    for plot in (plot for entry in scene.plots for plot in plots_in(entry)):
        for count in plot.step_counts:
            assert count == scene.step_count, (
                f"Plot '{plot.name}' has {count} steps, expected {scene.step_count}."
            )

    for info in scene.info:
        assert len(info.values) == scene.step_count, (
            f"Info row '{info.label}' has {len(info.values)} steps, "
            f"expected {scene.step_count}."
        )


def check_names(frames: Sequence[Frame]) -> None:
    expected = names_of(frames[0].renderings) if frames else []
    for step, frame in enumerate(frames):
        if (found := names_of(frame.renderings)) != expected:
            raise InconsistentRenderingsError(
                f"Step {step} renders {found}, but the first step renders {expected}. "
                f"Every step must render the same names in the same order."
            )


def names_of(renderings: Sequence[Rendering]) -> list[str]:
    return [rendering.name for rendering in renderings]
