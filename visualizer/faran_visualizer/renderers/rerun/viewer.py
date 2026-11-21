from typing import Sequence
from pathlib import Path
from tempfile import TemporaryDirectory
import shutil
import subprocess
import sys


def view(visualizations: Sequence[Path], *, in_browser: bool) -> None:
    """Opens the visualizations in the Rerun viewer and returns when it closes."""
    with TemporaryDirectory() as directory:
        copies = [
            copy_with_rerun_extension(visualization, index=index, into=Path(directory))
            for index, visualization in enumerate(visualizations)
        ]
        subprocess.run(
            [
                sys.executable,
                "-m",
                "rerun",
                *(str(copy) for copy in copies),
                *(["--web-viewer"] if in_browser else []),
            ],
            check=True,
        )


def copy_with_rerun_extension(visualization: Path, *, index: int, into: Path) -> Path:
    # NOTE: The viewer picks the file format by extension and does not know `.frn`.
    return Path(shutil.copy(visualization, into / f"{index}-{visualization.stem}.rrd"))
