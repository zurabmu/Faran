from typing import Sequence
from pathlib import Path
from tempfile import mkdtemp
import webbrowser

from faran_visualizer.renderers.canvas.page import page_html


def view(visualizations: Sequence[Path]) -> None:
    """Writes a page for each visualization to a temporary directory and opens it in
    the default browser. The pages stay there after the call returns."""
    directory = Path(mkdtemp(prefix="faran-visualizer-"))
    for visualization in visualizations:
        page = directory / f"{visualization.stem}.html"
        _ = page.write_text(
            page_html(
                visualization.read_text(encoding="utf-8"), title=visualization.stem
            ),
            encoding="utf-8",
        )
        _ = webbrowser.open(page.as_uri())
