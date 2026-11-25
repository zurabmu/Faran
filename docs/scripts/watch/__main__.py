from pathlib import Path

import typer
from watchfiles import watch

from .project import build_rules
from .rules import BuildRules
from .steps import Server


app = typer.Typer(add_completion=False)


@app.command(
    help=(
        "Serves the documentation site and, when a rule of the site changes, runs the "
        "steps that bring the site up to date, one at a time. Expects the site to be built."
    )
)
def main() -> None:
    server = Server()
    try:
        update_on_changes(build_rules(server))
    finally:
        server.stop()


def update_on_changes(build_rules: BuildRules) -> None:
    for changes in watch(*build_rules.paths):
        files = [Path(file) for _, file in changes]
        for step in build_rules.steps_for(files):
            step.run()


if __name__ == "__main__":
    app()
