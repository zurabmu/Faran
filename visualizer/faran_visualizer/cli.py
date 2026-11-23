from typing import Annotated
from pathlib import Path

from faran_visualizer.api import view
from faran_visualizer.renderers import CanvasRenderer, RerunRenderer

import typer

app = typer.Typer(
    name="faran-visualizer",
    help="Open visualizations of Faran simulations.",
    no_args_is_help=True,
)


@app.callback()
def commands() -> None:
    """Open visualizations of Faran simulations."""


@app.command("view")
def view_visualizations(
    visualizations: Annotated[
        list[Path], typer.Argument(help="Paths to visualization files.")
    ],
    browser: Annotated[
        bool,
        typer.Option("--browser", help="Open Rerun visualizations in the browser."),
    ] = False,
) -> None:
    """Open visualizations in a viewer."""
    view(
        visualizations,
        renderers=(RerunRenderer(in_browser=browser), CanvasRenderer()),
    )


def main() -> None:
    app()
