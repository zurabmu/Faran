from docs.extensions import EquationExtension

from markdown import Markdown


def test_that_equations_and_references_to_them_are_numbered_in_page_order() -> None:
    html = Markdown(
        extensions=[EquationExtension(), "pymdownx.arithmatex"],
        extension_configs={"pymdownx.arithmatex": {"generic": True}},
    ).convert(
        "/// equation | equation-first\n\n$$\nx = y\n$$\n\n///\n\n"
        "/// equation | equation-second\n\n$$\ny = z\n$$\n\n///\n\n"
        "See [](#equation-second)."
    )

    assert '<faran-equation id="equation-second" number="(2)">' in html
    assert '<a href="#equation-second">(2)</a>' in html
