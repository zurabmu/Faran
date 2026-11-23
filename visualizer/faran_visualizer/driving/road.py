from dataclasses import replace

from faran_visualizer.driving.styles import Styles
from faran_visualizer.scene import LinePattern, Points, Rendering


def road(
    *,
    surfaces: list[Points],
    edges_by_pattern: dict[LinePattern, list[Points]],
    styles: Styles,
) -> list[Rendering]:
    return [
        styles.road_surface.lines(name="road/surface", label="Road", strips=surfaces),
        *(
            replace(styles.lane_marking, pattern=pattern).lines(
                name=f"road/markings/{pattern}", label="Lane markings", strips=edges
            )
            for pattern, edges in edges_by_pattern.items()
        ),
    ]


def reference(points: Points, *, styles: Styles) -> Rendering:
    return styles.reference.lines(
        name="reference", label="Reference path", strips=[points]
    )


def boundaries(*, left: Points, right: Points, styles: Styles) -> Rendering:
    return styles.boundary.lines(
        name="boundaries", label="Corridor boundaries", strips=[left, right]
    )
