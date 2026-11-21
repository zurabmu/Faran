from typing import Final
from pathlib import Path

import rerun as rr

NOTEBOOK_VIEWER_HEIGHT: Final = 600


def show(visualization: Path) -> None:
    """Shows the visualization in the output of the current Jupyter notebook cell."""
    stream = rr.RecordingStream(application_id="faran")
    # NOTE: The loader picks the file format by the name's extension.
    stream.log_file_from_contents(
        f"{visualization.stem}.rrd", visualization.read_bytes()
    )
    stream.notebook_show(height=NOTEBOOK_VIEWER_HEIGHT)
