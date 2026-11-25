from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block


class DocsMapError(Exception):
    """Raised when a docs map block does not hold exactly one list of destinations."""


class DocsMapBlock(Block):
    """A map of the documentation that a planner drives through.

    Write `/// docs-map` around a list whose items each hold a link followed by a colon
    and a description. Any other content of the block appears below the map:

        /// docs-map

        - [Getting Started](guide/getting-started.md): Install Faran and run a planner.
        - [API Reference](api/index.md): Detailed usage instructions.

        Point at a section to see the planner find a path to it.

        ///
    """

    NAME = "docs-map"

    def on_create(self, parent: Element) -> Element:
        return SubElement(parent, "div", {"class": "faran-docs-map"})

    def on_end(self, block: Element) -> None:
        lists = [child for child in block if child.tag == "ul"]
        if len(lists) != 1:
            raise DocsMapError(
                "Expected a docs map block to hold exactly one list of destinations, "
                f"but it holds {len(lists)}."
            )
        (destinations,) = lists
        block.remove(destinations)
        docs_map = Element("faran-docs-map")
        docs_map.append(destinations)
        block.insert(0, docs_map)


class DocsMapExtension(BlocksExtension):
    """Adds the `/// docs-map` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(DocsMapBlock, self.getConfigs())


def makeExtension() -> DocsMapExtension:
    return DocsMapExtension()
