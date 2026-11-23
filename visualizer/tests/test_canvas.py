from pathlib import Path
from urllib.parse import urlparse
from urllib.request import url2pathname
import json

from faran_visualizer import (
    CanvasRenderer,
    Info,
    Scene,
    UnknownVisualizationError,
    render,
    show,
    view,
    visualizer,
)
from tests.dsl import files

from pytest import MonkeyPatch, raises

import numpy as np


async def test_that_canvas_renderer_saves_a_json_visualization(tmp_path: Path) -> None:
    visualize = visualizer.simulation(
        output="results", output_directory=tmp_path, renderer=CanvasRenderer()
    )

    await visualize(Scene(time_step=0.1, step_count=1), key="run")

    assert files.in_directory(tmp_path / "results") == ["run.json"]


async def test_that_canvas_visualization_holds_the_renderings_of_each_step(
    tmp_path: Path,
) -> None:
    visualize = visualizer.simulation(
        output="results", output_directory=tmp_path, renderer=CanvasRenderer()
    )
    scene = Scene(
        time_step=0.5,
        step_count=2,
        at_step=lambda step: [
            render.dots(
                name="robot",
                label="robot",
                positions=np.array([[float(step), 2.0]]),
                color="#ff000080",
            )
        ],
        info=[Info(label="Speed", values=np.array([1.0, 2.0]), unit="m/s")],
    )

    await visualize(scene, key="run")
    saved = json.loads((tmp_path / "results" / "run.json").read_text(encoding="utf-8"))

    assert saved["timeStep"] == 0.5
    assert [frame["renderings"][0]["positions"] for frame in saved["frames"]] == [
        [[0.0, 2.0]],
        [[1.0, 2.0]],
    ]
    assert saved["frames"][0]["renderings"][0]["style"]["color"] == [255, 0, 0, 128]
    assert saved["frames"][1]["info"] == [
        {"label": "Speed", "value": 2.0, "unit": "m/s"}
    ]


def test_that_canvas_frame_holds_its_renderings() -> None:
    frame = json.loads(
        CanvasRenderer.frame_json(
            renderings=[
                render.lines(
                    name="plan",
                    label="plan",
                    strips=[np.array([[0.0, 0.0], [1.0, 1.0]])],
                    color="#00ff00",
                    pattern="dashed",
                )
            ]
        )
    )

    assert frame == {
        "renderings": [
            {
                "kind": "lines",
                "name": "plan",
                "strips": [[[0.0, 0.0], [1.0, 1.0]]],
                "style": {"color": [0, 255, 0, 255], "width": 2.0, "pattern": "dashed"},
            }
        ],
        "info": [],
    }


async def test_that_viewing_a_canvas_visualization_opens_a_page_that_plays_it(
    tmp_path: Path, monkeypatch: MonkeyPatch
) -> None:
    opened: list[str] = []
    monkeypatch.setattr("webbrowser.open", lambda url: opened.append(url) or True)
    visualize = visualizer.simulation(
        output="results", output_directory=tmp_path, renderer=CanvasRenderer()
    )
    await visualize(Scene(time_step=0.1, step_count=1), key="run")

    view([tmp_path / "results" / "run.json"])

    (url,) = opened
    page = Path(url2pathname(urlparse(url).path)).read_text(encoding="utf-8")
    assert "FaranCanvas.mountAnimation" in page
    assert '"timeStep":0.1' in page


def test_that_unknown_visualization_extension_fails() -> None:
    with raises(UnknownVisualizationError, match=r"run\.txt.*'\.txt'"):
        show("run.txt")


async def test_that_canvas_visualization_holds_the_legend(tmp_path: Path) -> None:
    visualize = visualizer.simulation(
        output="results", output_directory=tmp_path, renderer=CanvasRenderer()
    )
    scene = Scene(
        time_step=0.1,
        step_count=1,
        at_step=lambda step: [
            render.lines(
                name="plan",
                label="Plan",
                strips=[np.array([[0.0, 0.0], [1.0, 1.0]])],
                color="#00ff00",
                pattern="dotted",
            ),
            render.dots(
                name="plan/points",
                label="Plan",
                positions=np.array([[0.0, 0.0]]),
                color="#00ff00",
                size=5.0,
            ),
        ],
    )

    await visualize(scene, key="run")
    saved = json.loads((tmp_path / "results" / "run.json").read_text(encoding="utf-8"))

    assert saved["legend"] == [
        {
            "label": "Plan",
            "marks": [
                {
                    "kind": "line",
                    "color": [0, 255, 0, 255],
                    "width": 2.0,
                    "pattern": "dotted",
                },
                {"kind": "dot", "color": [0, 255, 0, 255], "size": 5.0},
            ],
        }
    ]
