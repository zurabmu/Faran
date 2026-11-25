from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block


class ColumnsError(Exception):
    """Raised when a columns block does not have exactly one `---` line."""


class ColumnsBlock(Block):
    """Two columns side by side, which stack on narrow screens.

    Written as a `/// columns` block. A `---` line inside it separates the left column
    from the right one.
    """

    NAME = "columns"

    def on_create(self, parent: Element) -> Element:
        return SubElement(parent, "div", {"class": "faran-columns"})

    def on_end(self, block: Element) -> None:
        left, right = split_at_separator(list(block))
        remove_children(block)
        add_column(block, side="left", contents=left)
        add_column(block, side="right", contents=right)


class ColumnsExtension(BlocksExtension):
    """Adds the `/// columns` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(ColumnsBlock, self.getConfigs())


def split_at_separator(
    children: list[Element],
) -> tuple[list[Element], list[Element]]:
    separator = separator_index(children)
    return children[:separator], children[separator + 1 :]


def separator_index(children: list[Element]) -> int:
    separators = [index for index, child in enumerate(children) if is_separator(child)]
    if len(separators) != 1:
        raise ColumnsError(
            "Expected a columns block to have exactly one '---' line between its "
            f"columns, but it has {len(separators)}."
        )
    (separator,) = separators
    return separator


def is_separator(child: Element) -> bool:
    return child.tag == "hr"


def remove_children(block: Element) -> None:
    for child in list(block):
        block.remove(child)


def add_column(block: Element, *, side: str, contents: list[Element]) -> None:
    column = SubElement(block, "div", {"class": f"faran-columns__{side}"})
    column.extend(contents)


def makeExtension() -> ColumnsExtension:
    return ColumnsExtension()
