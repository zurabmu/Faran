from pathlib import Path

from docs.extensions import CitationExtension, CitationError

from markdown import Markdown
from pytest import fixture, raises

BIBTEX = """
@book{Thrun2005,
  title     = {Probabilistic Robotics},
  author    = {Thrun, Sebastian and Burgard, Wolfram and Fox, Dieter},
  publisher = {MIT Press},
  year      = {2005}
}
@book{Camacho2004,
  title     = {Model Predictive Control},
  author    = {Camacho, Eduardo F. and Bordons, Carlos},
  publisher = {Springer},
  year      = {2004}
}
"""


@fixture
def bib_file(tmp_path: Path) -> Path:
    path = tmp_path / "references.bib"
    _ = path.write_text(BIBTEX, encoding="utf-8")
    return path


def render(page: str, bib_file: Path) -> str:
    return Markdown(extensions=[CitationExtension(bib_file=str(bib_file))]).convert(
        page
    )


def test_that_citations_are_numbered_in_order_of_first_citation(
    bib_file: Path,
) -> None:
    html = render(
        "First[@Camacho2004], then[@Thrun2005], again[@Camacho2004].\n\n\\bibliography",
        bib_file,
    )

    assert html.count('href="#reference-Camacho2004">[1]</a>') == 2
    assert html.count('href="#reference-Thrun2005">[2]</a>') == 1


def test_that_bibliography_lists_only_cited_references(
    bib_file: Path,
) -> None:
    html = render("Cited[@Thrun2005].\n\n\\bibliography", bib_file)

    assert '<li id="reference-Thrun2005">' in html
    assert "Probabilistic Robotics" in html
    assert "Camacho2004" not in html


def test_that_citations_inside_code_blocks_stay_unchanged(bib_file: Path) -> None:
    html = render(
        "Cited[@Thrun2005].\n\n```\n[@Camacho2004]\n```\n\n\\bibliography", bib_file
    )

    assert "[@Camacho2004]" in html


def test_that_unknown_citation_key_fails(bib_file: Path) -> None:
    with raises(CitationError, match="Missing2020"):
        _ = render("Cited[@Missing2020].\n\n\\bibliography", bib_file)


def test_that_citing_without_bibliography_line_fails(bib_file: Path) -> None:
    with raises(CitationError, match="no '\\\\bibliography' line"):
        _ = render("Cited[@Thrun2005].", bib_file)


def test_that_bibliography_line_without_citations_fails(bib_file: Path) -> None:
    with raises(CitationError, match="cites nothing"):
        _ = render("No citations.\n\n\\bibliography", bib_file)
