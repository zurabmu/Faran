from typing import Final
from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from markdown.treeprocessors import Treeprocessor
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block

ELEMENT: Final = "faran-equation"
REFERENCE_PREFIX: Final = "#equation-"


class EquationError(Exception):
    """Raised when an equation block or a reference to an equation is invalid.

    An equation block is invalid if it does not have exactly one display formula,
    has a symbol that does not start with inline math, or has a reference to an
    id that no equation on the same page has.
    """


class EquationBlock(Block):
    """An equation followed by the definitions of its symbols.

    Write `/// equation | <id>` around one display formula and a list of its symbols.
    The id starts with `equation-`. Each list item starts with a symbol as inline math,
    followed by a sentence that says what the symbol stands for:

        /// equation | equation-mpc

        $$
        x_{t+1} = f(x_t, u_t)
        $$

        - $f$ is the dynamics model.
        - $u_t$ is the control input at step $t$.

        ///

    Equations are numbered in the order they appear on the page. To refer to one,
    write an empty link to its id, such as `equation [](#equation-mpc)`, which shows
    the equation's number. The equation must be on the same page as the link.
    """

    NAME = "equation"
    ARGUMENT = True

    def on_markdown(self) -> str:
        return "block"

    def on_create(self, parent: Element) -> Element:
        return SubElement(parent, ELEMENT, {"id": self.argument})

    def on_end(self, block: Element) -> None:
        formula_of(block).set("slot", "formula")
        for symbols in block.findall("ul"):
            symbols.set("slot", "symbols")

    def on_inline_end(self, block: Element) -> None:
        for item in block.iterfind("ul/li"):
            verify_starts_with_symbol(item, equation=self.argument)


class EquationNumbers(Treeprocessor):
    def run(self, root: Element) -> None:
        labels = number_equations(root)
        for link in root.iter("a"):
            if REFERENCE_PREFIX in link.get("href", ""):
                write_reference(link, labels)


class EquationExtension(BlocksExtension):
    """Adds the `/// equation` block, described in `EquationBlock`."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(EquationBlock, self.getConfigs())
        md.treeprocessors.register(EquationNumbers(md), "equation_numbers", 19)


def formula_of(equation: Element) -> Element:
    formulas = [child for child in equation if "arithmatex" in child.get("class", "")]
    if len(formulas) != 1:
        raise EquationError(
            f"Expected the equation '{equation.get('id')}' to hold one display "
            f"formula, but it holds {len(formulas)}."
        )
    (formula,) = formulas
    return formula


def verify_starts_with_symbol(item: Element, *, equation: str) -> None:
    first = item[0] if len(item) > 0 else None
    starts_with_symbol = (
        (item.text or "").strip() == ""
        and first is not None
        and "arithmatex" in first.get("class", "")
    )
    if not starts_with_symbol:
        raise EquationError(
            f"Expected every item in the symbol list of the equation '{equation}' to "
            f"start with inline math, but one starts with "
            f"'{''.join(item.itertext())[:40]}'."
        )


def number_equations(root: Element) -> dict[str, str]:
    labels: dict[str, str] = {}
    for number, equation in enumerate(root.iter(ELEMENT), start=1):
        label = f"({number})"
        equation.set("number", label)
        labels[f"#{equation.get('id')}"] = label
    return labels


def write_reference(link: Element, labels: dict[str, str]) -> None:
    href = link.get("href", "")
    if href not in labels:
        raise EquationError(
            f"Expected the equation reference '{href}' to link to an equation on the "
            f"same page, but the page has only {', '.join(labels) or 'no equations'}."
        )
    link.text = labels[href]


def makeExtension() -> EquationExtension:
    return EquationExtension()
