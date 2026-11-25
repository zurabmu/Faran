from pathlib import Path
from shutil import copy2
from zipfile import ZipFile
from subprocess import run
from tempfile import mkdtemp
from typing import Final

import typer

OUTPUT: Final = Path("docs/content/assets/pyodide")
VISUALIZER: Final = Path("visualizer")
LAB: Final = Path("docs/lab")
LAB_ARCHIVE: Final = OUTPUT / "lab.zip"

app = typer.Typer(add_completion=False)


@app.command(
    help=(
        "Builds Faran and Faran visualizer wheels from the current source and zips the "
        f"{LAB} package into {OUTPUT}, for the home page to load in Pyodide."
    )
)
def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    publish(built_wheel(project=Path("."), name="faran"), manifest="faran-wheel.txt")
    publish(
        built_wheel(project=VISUALIZER, name="faran_visualizer"),
        manifest="visualizer-wheel.txt",
    )
    publish_lab()


def built_wheel(*, project: Path, name: str) -> Path:
    directory = Path(mkdtemp(prefix=f"{name}-wheel-"))
    run(
        ["uv", "build", "--wheel", "--out-dir", str(directory.resolve())],
        check=True,
        cwd=project,
    )
    wheels = list(directory.glob(f"{name}-*.whl"))
    assert len(wheels) == 1, f"Expected one {name} wheel, but found {wheels}."
    return wheels[0]


def publish(wheel: Path, *, manifest: str) -> None:
    prefix = wheel.name.split("-")[0]
    for previous in OUTPUT.glob(f"{prefix}-*.whl"):
        previous.unlink()

    copy2(wheel, OUTPUT / wheel.name)
    (OUTPUT / manifest).write_text(wheel.name, encoding="utf-8")
    print(f"Wrote {OUTPUT / wheel.name}")


def publish_lab() -> None:
    with ZipFile(LAB_ARCHIVE, "w") as archive:
        for module in sorted(LAB.glob("*.py")):
            archive.write(module, f"lab/{module.name}")
    print(f"Wrote {LAB_ARCHIVE}")


if __name__ == "__main__":
    app()
