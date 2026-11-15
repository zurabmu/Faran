import re
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any, Final

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor
from pybtex.backends.html import Backend as HtmlBackend
from pybtex.database import BibliographyData, parse_file
from pybtex.style.formatting.plain import Style as PlainStyle

CITATION: Final = re.compile(r"\[@([^\]\s]+)\]")
BIBLIOGRAPHY_MARKER: Final = "\\bibliography"
FENCE: Final = re.compile(r"^\s*(```|~~~)")


class CitationError(Exception):
    """Raised when a page's citations do not match the bibliography."""


class CitationExtension(Extension):
    """Turns `[@key]` into numbered links and `\\bibliography` into a reference list.

    Numbers follow the order in which a page first cites each key. A page that cites
    a key missing from the BibTeX file, cites without a `\\bibliography` line, or has
    that line without citing anything raises `CitationError`.
    """

    def __init__(self, **kwargs: Any) -> None:
        self.config = {"bib_file": ["docs/references.bib", "Path to the BibTeX file."]}
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        bibliography = parse_file(Path(self.getConfig("bib_file")), bib_format="bibtex")
        md.preprocessors.register(
            CitationPreprocessor(md, bibliography), "citations", 30
        )


class CitationPreprocessor(Preprocessor):
    def __init__(self, md: Markdown, bibliography: BibliographyData) -> None:
        super().__init__(md)
        self.bibliography = bibliography

    def run(self, lines: list[str]) -> list[str]:
        keys = cited_keys(lines)
        self.verify_known(keys)
        verify_bibliography_marker(lines, keys)
        numbers = {key: number for number, key in enumerate(keys, start=1)}
        return list(self.replace_citations(lines, numbers))

    def verify_known(self, keys: Iterable[str]) -> None:
        for key in keys:
            if key not in self.bibliography.entries:
                raise CitationError(
                    f"Citation key '{key}' is not in the bibliography. "
                    f"Expected one of: {', '.join(sorted(self.bibliography.entries))}."
                )

    def replace_citations(
        self, lines: list[str], numbers: dict[str, int]
    ) -> Iterable[str]:
        for line, is_code in with_code_flags(lines):
            if is_code:
                yield line
            elif is_bibliography_marker(line):
                yield self.reference_list(numbers)
            else:
                yield CITATION.sub(lambda match: citation_link(match[1], numbers), line)

    def reference_list(self, numbers: dict[str, int]) -> str:
        items = "".join(
            f'<li id="{reference_id(key)}">{self.formatted_entry(key)}</li>'
            for key in numbers
        )
        return self.md.htmlStash.store(f'<ol class="faran-references">{items}</ol>')

    def formatted_entry(self, key: str) -> str:
        entry = PlainStyle().format_entry(key, self.bibliography.entries[key])
        return entry.text.render(HtmlBackend())


def cited_keys(lines: list[str]) -> list[str]:
    keys: dict[str, None] = {}
    for line, is_code in with_code_flags(lines):
        if not is_code:
            keys.update((key, None) for key in CITATION.findall(line))
    return list(keys)


def verify_bibliography_marker(lines: Sequence[str], keys: Sequence[str]) -> None:
    has_marker = any(is_bibliography_marker(line) for line in lines)
    if keys and not has_marker:
        raise CitationError(
            f"Page cites {', '.join(keys)} but has no '{BIBLIOGRAPHY_MARKER}' line. "
            "Expected a line where the reference list goes."
        )
    if has_marker and not keys:
        raise CitationError(
            f"Page has a '{BIBLIOGRAPHY_MARKER}' line but cites nothing. "
            "Expected at least one [@key] citation."
        )


def is_bibliography_marker(line: str) -> bool:
    return line.strip() == BIBLIOGRAPHY_MARKER


def with_code_flags(lines: Iterable[str]) -> Iterable[tuple[str, bool]]:
    inside_fence = False
    for line in lines:
        is_fence = FENCE.match(line) is not None
        yield line, inside_fence or is_fence
        inside_fence = inside_fence != is_fence


def citation_link(key: str, numbers: dict[str, int]) -> str:
    return f'<a class="faran-citation" href="#{reference_id(key)}">[{numbers[key]}]</a>'


def reference_id(key: str) -> str:
    return f"reference-{key}"


def makeExtension(**kwargs: Any) -> CitationExtension:
    return CitationExtension(**kwargs)
