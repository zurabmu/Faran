from typing import Final
from pathlib import Path
from html import escape

from faran_visualizer.renderers.canvas.page import page_html

NOTEBOOK_VIEWER_HEIGHT: Final = 600


def show(visualization: Path) -> None:
    """Shows the visualization in the output of the current Jupyter notebook cell."""
    from IPython.display import HTML, display

    page = page_html(
        visualization.read_text(encoding="utf-8"), title=visualization.stem
    )
    display(
        HTML(
            f'<iframe srcdoc="{escape(page)}" style="width:100%;border:0" '
            f'height="{NOTEBOOK_VIEWER_HEIGHT}"></iframe>'
        )
    )
