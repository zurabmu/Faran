import sys
from pathlib import Path
from typing import Final

from .rules import BuildRules, BuildRule
from .steps import Command, Server

PYTHON: Final = frozenset({".py"})
WEB: Final = frozenset({".ts", ".svelte", ".css"})


def build_rules(server: Server) -> BuildRules:
    """Returns the build rules of this repository, with `server` as the step that restarts
    the docs server."""
    engine = pnpm_build(
        name="the canvas engine build", directory=Path("visualizer/engine")
    )
    ui = pnpm_build(name="the docs components build", directory=Path("docs/ui"))
    wheel = python(
        name="the Pyodide wheel build", arguments=("-m", "docs.scripts.wheel")
    )
    examples = python(
        name="the docs examples",
        arguments=("-m", "pytest", "-m", "docs", "--visualize"),
    )
    rebuilt_code = (wheel, examples, server)
    return BuildRules(
        rules=[
            BuildRule(
                path=Path("visualizer/engine/src"),
                suffixes=WEB,
                steps=(engine, ui, wheel, server),
            ),
            BuildRule(path=Path("docs/ui/src"), suffixes=WEB, steps=(ui, server)),
            BuildRule(path=Path("docs/ui/scripts"), suffixes=WEB, steps=(ui, server)),
            BuildRule(path=Path("faran"), suffixes=PYTHON, steps=rebuilt_code),
            BuildRule(
                path=Path("visualizer/faran_visualizer"),
                suffixes=frozenset({".py", ".html"}),
                steps=rebuilt_code,
            ),
            BuildRule(path=Path("docs/lab"), suffixes=PYTHON, steps=(wheel,)),
            BuildRule(
                path=Path("docs/examples"), suffixes=PYTHON, steps=(examples, server)
            ),
            BuildRule(path=Path("docs/snippets"), suffixes=PYTHON, steps=(server,)),
            BuildRule(
                path=Path("docs/extensions"),
                suffixes=frozenset({".py", ".csl"}),
                steps=(server,),
            ),
            BuildRule(
                path=Path("zensical.toml"),
                suffixes=frozenset({".toml"}),
                steps=(server,),
            ),
            BuildRule(
                path=Path("docs/features.yaml"),
                suffixes=frozenset({".yaml"}),
                steps=(server,),
            ),
            BuildRule(
                path=Path("docs/references.bib"),
                suffixes=frozenset({".bib"}),
                steps=(server,),
            ),
        ],
        order=(engine, ui, wheel, examples, server),
    )


def pnpm_build(*, name: str, directory: Path) -> Command:
    return Command(name=name, program="pnpm", arguments=("build",), directory=directory)


def python(*, name: str, arguments: tuple[str, ...]) -> Command:
    return Command(
        name=name, program=sys.executable, arguments=arguments, directory=Path(".")
    )
