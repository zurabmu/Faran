from dataclasses import dataclass

from faran_visualizer.scene import (
    Animation,
    Chart,
    Color,
    Dots,
    DotStyle,
    LegendEntry,
    Lines,
    LineStyle,
    PlotLine,
    Rendering,
)

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

    def color_of(self, *, at: str, step: int) -> str:
        """Returns the color of the named rendering at the step, as `#rrggbbaa`."""
        rendering = self._rendering(at, step=step)
        return hex_of(rendering.style.color)

    def plot_line_color(self, *, at: str) -> str:
        """Returns the color of the plot line with the name in its legend, as
        `#rrggbbaa`."""
        return hex_of(self._plot_line(at).style.color)

    def background_color(self) -> str:
        """Returns the color behind the scene and the charts, as `#rrggbbaa`."""
        return hex_of(self.animation.background_color)

    def info(self, *, at: str, step: int) -> float:
        """Returns the value of the labeled row of the info table at the step."""
        (row,) = [row for row in self.animation.frames[step].info if row.label == at]
        return row.value

    def legend(self) -> list[str]:
        """Returns the labels of the legend entries, in legend order."""
        return [entry.label for entry in self.animation.legend]

    def legend_sample(self, *, at: str) -> list[str]:
        """Returns how the sample of the labeled legend entry is drawn, one
        description per style, such as `dashed line #ff0000ff` or `dot #ff0000ff`."""
        return [description_of(style) for style in self._legend_entry(at).styles]

    def _legend_entry(self, label: str) -> LegendEntry:
        (entry,) = [entry for entry in self.animation.legend if entry.label == label]
        return entry

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


def hex_of(color: Color) -> str:
    return "#" + "".join(f"{channel:02x}" for channel in color)


def description_of(style: LineStyle | DotStyle) -> str:
    match style:
        case LineStyle(color=color, pattern=pattern):
            return f"{pattern} line {hex_of(color)}"
        case DotStyle(color=color):
            return f"dot {hex_of(color)}"
