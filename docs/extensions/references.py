import re
from collections.abc import Mapping, Sequence
from html import escape
from pathlib import Path
from typing import Final, NamedTuple, TypedDict

from citeproc import (
    Citation,
    CitationItem,
    CitationStylesBibliography,
    CitationStylesStyle,
    formatter,
)
from citeproc.source.json import CiteProcJSON
from pybtex.database import BibliographyData, Entry, Person
from pybtex.richtext import Text

STYLE: Final = Path(__file__).with_name("ieee.csl")
NUMBER_LABEL: Final = re.compile(r"^\[\d+\]")
CSL_TYPES: Final = {
    "article": "article-journal",
    "inproceedings": "paper-conference",
    "incollection": "chapter",
    "book": "book",
    "techreport": "report",
    "phdthesis": "thesis",
    "misc": "article",
}
CSL_VARIABLES: Final = {
    "title": "title",
    "journal": "container-title",
    "booktitle": "container-title",
    "publisher": "publisher",
    "institution": "publisher",
    "address": "publisher-place",
    "volume": "volume",
    "number": "issue",
    "pages": "page",
    "edition": "edition",
    "doi": "DOI",
    "url": "URL",
}


class CslName(TypedDict):
    given: str
    family: str


CslDate = TypedDict("CslDate", {"date-parts": list[list[int]]})

type CslValue = str | list[CslName] | CslDate


class Link(NamedTuple):
    text: str
    href: str


def formatted_references(
    bibliography: BibliographyData, keys: Sequence[str]
) -> list[str]:
    """Returns the IEEE-style HTML of each entry, in the order of `keys`, without its
    `[n]` label. DOIs and URLs are links."""
    entries = {key: bibliography.entries[key] for key in keys}
    return [
        with_links(with_commas_inside_quotes(without_label(text)), entry)
        for text, entry in zip(ieee_references(entries), entries.values(), strict=True)
    ]


def ieee_references(entries: dict[str, Entry]) -> list[str]:
    style = CitationStylesStyle(str(STYLE), validate=False)
    source = CiteProcJSON([csl_item(key, entry) for key, entry in entries.items()])
    references = CitationStylesBibliography(style, source, formatter.html)
    for key in entries:
        references.register(Citation([CitationItem(key)]))
    return [str(text) for text in references.bibliography()]


def csl_item(key: str, entry: Entry) -> dict[str, CslValue]:
    return {
        "id": key,
        "type": CSL_TYPES[type_of(entry)],
        "author": [csl_name(person) for person in persons_of(entry, role="author")],
        "issued": {"date-parts": [[int(field(entry, "year"))]]},
        **csl_variables(entry),
    }


def csl_variables(entry: Entry) -> dict[str, str]:
    variables = {
        name: plain_text(value)
        for bibtex_name, name in CSL_VARIABLES.items()
        if (value := field(entry, bibtex_name))
    }
    if entry.type == "techreport":
        variables["genre"] = "Tech. Rep."
    if is_arxiv(entry):
        variables["number"] = arxiv_id(entry)
        del variables["URL"]
    return variables


def csl_name(person: Person) -> CslName:
    return CslName(
        given=plain_text(" ".join(person.bibtex_first_names)),
        family=plain_text(" ".join(family_names_of(person))),
    )


def plain_text(latex: str) -> str:
    return Text.from_latex(latex).render_as("text")


def is_arxiv(entry: Entry) -> bool:
    return field(entry, "archiveprefix").lower() == "arxiv"


def arxiv_id(entry: Entry) -> str:
    return f"arXiv:{fields_of(entry)['eprint']}"


def without_label(text: str) -> str:
    assert NUMBER_LABEL.match(text), (
        f"Expected the IEEE style to start each reference with its [n] label, but got: {text}"
    )
    return NUMBER_LABEL.sub("", text, count=1).strip()


def with_commas_inside_quotes(text: str) -> str:
    # citeproc-py ignores the locale's punctuation-in-quote rule, which IEEE follows.
    return text.replace("”,", ",”")


def with_links(text: str, entry: Entry) -> str:
    for link in links(entry):
        text = text.replace(escape(link.text), anchor(link), 1)
    return text


def links(entry: Entry) -> list[Link]:
    if doi := field(entry, "doi"):
        return [Link(text=doi, href=f"https://doi.org/{doi}")]
    if is_arxiv(entry):
        return [Link(text=arxiv_id(entry), href=field(entry, "url"))]
    if url := field(entry, "url"):
        return [Link(text=url, href=url)]
    return []


def field(entry: Entry, name: str) -> str:
    return fields_of(entry).get(name, "").strip()


def anchor(link: Link) -> str:
    return f'<a href="{escape(link.href)}">{escape(link.text)}</a>'


def type_of(entry: Entry) -> str:
    assert entry.type is not None, (
        f"Expected the BibTeX entry {entry.key} to have a type."
    )
    return entry.type


def fields_of(entry: Entry) -> Mapping[str, str]:
    assert entry.fields is not None, (
        f"Expected the BibTeX entry {entry.key} to have fields."
    )
    return entry.fields


def persons_of(entry: Entry, *, role: str) -> list[Person]:
    assert entry.persons is not None, (
        f"Expected the BibTeX entry {entry.key} to have persons."
    )
    return entry.persons.get(role, [])


def family_names_of(person: Person) -> list[str]:
    assert person.prelast_names is not None and person.last_names is not None, (
        f"Expected the BibTeX person {person} to have prelast and last names."
    )
    return person.prelast_names + person.last_names
