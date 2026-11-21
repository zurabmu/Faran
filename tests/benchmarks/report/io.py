import asyncio
import glob
from pathlib import Path

from .models import BenchmarkData, ExportData

from rich.console import Console

import anyio
import msgspec


def resolve(filepath: str, console: Console) -> Path:
    if (path := Path(filepath)).exists():
        return path

    if matches := glob.glob(filepath):
        resolved = Path(sorted(matches)[-1])
        console.print(f"[dim]Using: {resolved}[/dim]\n")
        return resolved

    raise FileNotFoundError(f"No file found: {filepath}")


async def load(path: Path) -> BenchmarkData:
    content = await anyio.Path(path).read_bytes()
    return msgspec.json.decode(content, type=BenchmarkData, strict=False)


async def load_many(paths: list[Path]) -> list[tuple[Path, BenchmarkData]]:
    async def load_one(path: Path) -> tuple[Path, BenchmarkData]:
        return (path, await load(path))

    return await asyncio.gather(*[load_one(path) for path in paths])


async def save_html(path: Path, html_console: Console, console: Console) -> None:
    html_content = html_console.export_html(inline_styles=True)
    await anyio.Path(path).write_text(html_content, encoding="utf-8")

    console.print(f"[green]HTML report saved to: {path}[/green]")


async def save_json(path: Path, export_data: ExportData, console: Console) -> None:
    json_data = {
        "machine_info": export_data.machine_info,
        "commit_info": export_data.commit_info,
        "benchmarks": [
            {
                "name": benchmark.name,
                "group": benchmark.group,
                "implementation": benchmark.implementation,
                "parameters": benchmark.parameters,
                "mean_seconds": benchmark.mean,
                "min_seconds": benchmark.min,
                "max_seconds": benchmark.max,
                "stddev_seconds": benchmark.stddev,
                "median_seconds": benchmark.median,
                "rounds": benchmark.rounds,
                "ops": benchmark.ops,
                "iqr_seconds": benchmark.iqr,
            }
            for benchmark in export_data.benchmarks
        ],
        "summary": export_data.summary,
    }
    encoded = msgspec.json.encode(json_data)

    await anyio.Path(path).write_bytes(encoded)

    console.print(f"[green]JSON data saved to: {path}[/green]")
