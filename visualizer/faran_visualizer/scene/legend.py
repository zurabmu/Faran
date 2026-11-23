from typing import Final, Sequence
from dataclasses import replace

from faran_visualizer.scene.animation import (
    Color,
    DotStyle,
    LegendEntry,
    LineStyle,
    Rendering,
)

MINIMUM_SAMPLE_ALPHA: Final = 128


def legend_of(renderings: Sequence[Rendering]) -> list[LegendEntry]:
    labels = dict.fromkeys(rendering.label for rendering in renderings)
    return [entry_of(label, renderings=renderings) for label in labels]


def entry_of(label: str, *, renderings: Sequence[Rendering]) -> LegendEntry:
    styles = [rendering.style for rendering in renderings if rendering.label == label]
    line_styles = [style for style in styles if isinstance(style, LineStyle)]
    dot_styles = [style for style in styles if isinstance(style, DotStyle)]
    return LegendEntry(
        label=label,
        styles=[sample_style(style) for style in [*line_styles[:1], *dot_styles[:1]]],
    )


def sample_style[S: (LineStyle, DotStyle)](style: S) -> S:
    return replace(style, color=visible(style.color))


def visible(color: Color) -> Color:
    return color._replace(alpha=max(color.alpha, MINIMUM_SAMPLE_ALPHA))
