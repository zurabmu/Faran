from dataclasses import replace

from faran_visualizer.driving.styles import styles
from faran_visualizer.scene import LinePattern, Points, Rendering


def road(
    *, surfaces: list[Points], edges_by_pattern: dict[LinePattern, list[Points]]
) -> list[Rendering]:
    return [
        styles.road_surface.lines(name="road/surface", strips=surfaces),
        *(
            replace(styles.lane_marking, pattern=pattern).lines(
                name=f"road/markings/{pattern}", strips=edges
            )
            for pattern, edges in edges_by_pattern.items()
        ),
    ]


def reference(points: Points) -> Rendering:
    return styles.reference.lines(name="reference", strips=[points])


def boundaries(*, left: Points, right: Points) -> Rendering:
    return styles.boundary.lines(name="boundaries", strips=[left, right])
