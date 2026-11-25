from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block


class HeroBlock(Block):
    """The header of a page: the animated Faran mark above the block's content, centered
    on the first screen. Links with the class `faran-button` show as buttons, and
    `faran-button--primary` marks the main one:

        /// hero

        # Composable Trajectory Planning for Python

        Build trajectory planners from modular components.

        [Get Started](guide/getting-started.md){ .faran-button .faran-button--primary }
        [Examples](guide/examples/index.md){ .faran-button }

        ///
    """

    NAME = "hero"

    def on_create(self, parent: Element) -> Element:
        hero = SubElement(
            parent, "section", {"class": "faran-hero", "data-water-strength": "1"}
        )
        SubElement(hero, "faran-mark", {"class": "faran-hero__mark", "animate": ""})
        return hero


class HeroExtension(BlocksExtension):
    """Adds the `/// hero` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(HeroBlock, self.getConfigs())


def makeExtension() -> HeroExtension:
    return HeroExtension()
