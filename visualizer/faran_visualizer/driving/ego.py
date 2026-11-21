from faran_visualizer.driving.shapes import Poses, Shape
from faran_visualizer.driving.styles import styles
from faran_visualizer.scene import Points, Rendering


def traveled_path(positions: Points) -> Rendering:
    return styles.traveled_path.lines(name="ego/path", strips=[positions])


def ego_body(pose: Poses, *, shape: Shape) -> list[Rendering]:
    return [
        styles.ego.lines(name="ego/body", strips=list(shape.outlines(pose))),
        styles.ego_heading.lines(
            name="ego/heading", strips=list(shape.heading_lines(pose))
        ),
    ]


def ghost(positions: Points) -> Rendering:
    return styles.ghost.dots(name="ego/ghost", positions=positions)
