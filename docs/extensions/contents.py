from typing import Final, TypedDict, cast

from markdown import Extension, Markdown
from markdown.postprocessors import Postprocessor

API_SYMBOL: Final = "doc-symbol-heading"
PAGE_TITLE_LEVEL: Final = 1


class TocEntry(TypedDict):
    level: int
    html: str
    children: list["TocEntry"]


class ContentsExtension(Extension):
    """Gives the table of contents the same structure as the site navigation.

    Each API entry that follows a section heading at the top level of the table of
    contents, or at the level directly below the page title, is a child of that
    heading's entry.
    """

    def extendMarkdown(self, md: Markdown) -> None:
        md.postprocessors.register(ContentsPostprocessor(md), "faran_contents", 1)


class ContentsPostprocessor(Postprocessor):
    def run(self, text: str) -> str:
        entries = toc_entries_of(self.md)
        entries[:] = with_api_entries_as_children_of_sections(entries)
        for entry in entries:
            if entry["level"] == PAGE_TITLE_LEVEL:
                entry["children"] = with_api_entries_as_children_of_sections(
                    entry["children"]
                )
        return text


def toc_entries_of(md: Markdown) -> list[TocEntry]:
    # Python-Markdown declares no type for the entries its toc extension stores.
    return cast(list[TocEntry], vars(md)["toc_tokens"])


def with_api_entries_as_children_of_sections(
    entries: list[TocEntry],
) -> list[TocEntry]:
    arranged: list[TocEntry] = []
    for entry in entries:
        follows_section = len(arranged) > 0 and not is_api_entry(arranged[-1])
        if is_api_entry(entry) and follows_section:
            arranged[-1]["children"].append(entry)
        else:
            arranged.append(entry)
    return arranged


def is_api_entry(entry: TocEntry) -> bool:
    return API_SYMBOL in entry["html"]


def makeExtension() -> ContentsExtension:
    return ContentsExtension()
