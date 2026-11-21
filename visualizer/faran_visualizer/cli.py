from typing import Annotated
from pathlib import Path

from faran_visualizer.api import view

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
    visualizations: Annotated[list[Path], typer.Argument(help="Paths to .frn files.")],
    browser: Annotated[
        bool, typer.Option("--browser", help="Open the viewer in the browser.")
    ] = False,
) -> None:
    """Open visualizations in a viewer."""
    view(visualizations, in_browser=browser)


def main() -> None:
    app()
