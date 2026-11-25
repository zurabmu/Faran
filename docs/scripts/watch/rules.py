from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .steps import Step


@dataclass(frozen=True, kw_only=True)
class BuildRule:
    """Files under `path` with one of `suffixes`, and the steps a change to them calls for.
    `path` is relative to the working directory, and is a directory or a single file."""

    path: Path
    suffixes: frozenset[str]
    steps: Sequence[Step]

    def contains_any(self, files: Sequence[Path]) -> bool:
        return any(self.contains(file) for file in files)

    def contains(self, file: Path) -> bool:
        return file.is_relative_to(self.path.resolve()) and file.suffix in self.suffixes


@dataclass(frozen=True, kw_only=True)
class BuildRules:
    """The build rules of the documentation site, and all of their steps in the order they run in."""

    rules: Sequence[BuildRule]
    order: Sequence[Step]

    def __post_init__(self) -> None:
        for rule in self.rules:
            for step in rule.steps:
                assert step in self.order, (
                    f"Expected every step of the rule {rule.path} in the step order, "
                    f"but {step} is missing."
                )

    @property
    def paths(self) -> list[Path]:
        return [rule.path for rule in self.rules]

    def steps_for(self, files: Sequence[Path]) -> list[Step]:
        """Returns the steps that changes to the absolute paths `files` call for, each once."""
        needed = [
            step
            for rule in self.rules
            if rule.contains_any(files)
            for step in rule.steps
        ]
        return [step for step in self.order if step in needed]
