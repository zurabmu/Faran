from dataclasses import dataclass

from faran_visualizer.scene import Animation, Chart, Dots, Lines, PlotLine, Rendering

import numpy as np


@dataclass(frozen=True)
class Visualization:
    """Looks up what a visualizer hands to its renderer, by the names a user sees."""

    animation: Animation

    def lines(self, *, at: str, step: int) -> list[list[list[float]]]:
        """Returns the strips of the named rendering at the step."""
        lines = self._rendering(at, step=step)
        assert isinstance(lines, Lines), f"Expected {at} to render lines, got {lines}."
        return [np.asarray(strip).tolist() for strip in lines.strips]

    def dots(self, *, at: str, step: int) -> list[list[float]]:
        """Returns the positions of the named rendering at the step."""
        dots = self._rendering(at, step=step)
        assert isinstance(dots, Dots), f"Expected {at} to render dots, got {dots}."
        return np.asarray(dots.positions).tolist()

    def plot_line(self, *, at: str) -> list[float]:
        """Returns the values of the plot line with the name in its legend."""
        return np.asarray(self._plot_line(at).values).tolist()

    def plot_of(self, *, at: str) -> str:
        """Returns the plot that the named plot line is rendered in. Lines rendered
        together return the same plot."""
        return self._chart_of(at).id

    def plot_line_names(self) -> list[str]:
        """Returns the legend names of every plot line, sorted."""
        return sorted(
            line.name for chart in self.animation.charts for line in chart.lines
        )

    def info(self, *, at: str, step: int) -> float:
        """Returns the value of the labeled row of the info table at the step."""
        (row,) = [row for row in self.animation.frames[step].info if row.label == at]
        return row.value

    def _rendering(self, name: str, *, step: int) -> Rendering:
        matches = [
            rendering
            for rendering in [
                *self.animation.background,
                *self.animation.frames[step].renderings,
            ]
            if rendering.name == name
        ]
        assert len(matches) == 1, (
            f"Expected one rendering named {name} at step {step}, found {len(matches)}."
        )
        return matches[0]

    def _plot_line(self, name: str) -> PlotLine:
        (line,) = [line for line in self._chart_of(name).lines if line.name == name]
        return line

    def _chart_of(self, name: str) -> Chart:
        matches = [
            chart
            for chart in self.animation.charts
            if any(line.name == name for line in chart.lines)
        ]
        assert len(matches) == 1, (
            f"Expected one plot with a line named {name}, found {len(matches)}."
        )
        return matches[0]
