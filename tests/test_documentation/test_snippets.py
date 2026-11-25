from pathlib import Path

import msgspec

from docs.lab import SnippetVisualizationError, run_snippet

from pytest import mark, raises


class Visualization(msgspec.Struct):
    frames: list[msgspec.Raw]


def snippets() -> list[Path]:
    return sorted(Path("docs/snippets").glob("*.py"))


@mark.docs
@mark.asyncio
@mark.parametrize("snippet", snippets(), ids=lambda path: path.stem)
async def test_that_documentation_snippet_saves_one_visualization(
    snippet: Path,
) -> None:
    visualization = msgspec.json.decode(
        await run_snippet(snippet.read_text(encoding="utf-8")), type=Visualization
    )

    assert len(visualization.frames) > 0


@mark.asyncio
async def test_that_snippet_runner_rejects_snippet_without_visualization() -> None:
    with raises(SnippetVisualizationError, match="saved 0"):
        await run_snippet("x = 1")
