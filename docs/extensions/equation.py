from typing import Any
from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block


class EquationBlock(Block):
    """An equation plate: a display formula followed by the list of its symbols.

    Written as `/// equation | <id>`, where the id is what a link to the plate uses.
    """

    NAME = "equation"
    ARGUMENT = True

    def on_create(self, parent: Element) -> Element:
        return SubElement(
            parent, "div", {"class": "faran-equation", "id": self.argument}
        )


class EquationExtension(BlocksExtension):
    """Adds the `/// equation` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(EquationBlock, self.getConfigs())


def makeExtension(**kwargs: Any) -> EquationExtension:
    return EquationExtension(**kwargs)
