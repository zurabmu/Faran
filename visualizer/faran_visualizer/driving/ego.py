from faran_visualizer.driving.shapes import Poses, Shape
from faran_visualizer.driving.styles import Styles
from faran_visualizer.scene import Points, Rendering


def traveled_path(positions: Points, *, styles: Styles) -> Rendering:
    return styles.traveled_path.lines(
        name="ego/path", label="Traveled path", strips=[positions]
    )


def ego_body(pose: Poses, *, shape: Shape, styles: Styles) -> list[Rendering]:
    return [
        styles.ego.lines(
            name="ego/body", label="Ego vehicle", strips=list(shape.outlines(pose))
        ),
        styles.ego_heading.lines(
            name="ego/heading",
            label="Ego vehicle",
            strips=list(shape.heading_lines(pose)),
        ),
    ]


def ghost(positions: Points, *, styles: Styles) -> Rendering:
    return styles.ghost.dots(
        name="ego/ghost", label="Path progress", positions=positions
    )
