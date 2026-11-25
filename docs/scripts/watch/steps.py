import sys
from dataclasses import dataclass
from pathlib import Path
from shutil import which
from subprocess import Popen, run
from typing import Protocol, Sequence


class Step(Protocol):
    """A step that brings part of the documentation site up to date."""

    def run(self) -> None:
        """Runs the step. A failed step reports the failure and returns."""
        ...


@dataclass(frozen=True, kw_only=True)
class Command:
    """Runs a program in a directory."""

    name: str
    program: str
    arguments: Sequence[str]
    directory: Path

    def run(self) -> None:
        report(f"Running {self.name}")
        result = run([executable(self.program), *self.arguments], cwd=self.directory)
        if result.returncode != 0:
            report(f"{self.name} failed with exit code {result.returncode}")


class Server:
    """Runs `zensical serve`. Running it as a step restarts the server."""

    def __init__(self) -> None:
        self.process = start_server()

    def run(self) -> None:
        report("Restarting the docs server")
        self.stop()
        self.process = start_server()

    def stop(self) -> None:
        """Stops the server and waits until it has exited."""
        self.process.terminate()
        self.process.wait()


def start_server() -> Popen[bytes]:
    return Popen([sys.executable, "-m", "zensical", "serve"])


def executable(program: str) -> str:
    path = which(program)
    assert path is not None, f"Expected {program} on the PATH, but it is missing."
    return path


def report(message: str) -> None:
    print(f"[docs-watch] {message}", flush=True)
