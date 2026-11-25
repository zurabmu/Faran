from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block

HEADINGS = ("h2", "h3", "h4")


class GalleryError(Exception):
    """Raised when a gallery block does not start with a heading."""


class GalleryBlock(Block):
    """A gallery that shows one of its sections at a time and moves on by itself.

    Write `/// gallery` around sections that each start with a heading. The heading's
    text names the section's tab:

        /// gallery

        ### Composable

        Text and code of the first section.

        ### Tested

        Text and code of the second section.

        ///
    """

    NAME = "gallery"

    def on_markdown(self) -> str:
        return "block"

    def on_create(self, parent: Element) -> Element:
        return SubElement(parent, "faran-gallery", {"data-water-ignores-presses": ""})

    def on_end(self, block: Element) -> None:
        children = detach_children_of(block)
        ensure_first_is_heading(children)
        for child in children:
            if is_heading(child):
                add_section_to(block)
            add_to_last_section_of(block, child)


class GalleryExtension(BlocksExtension):
    """Adds the `/// gallery` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(GalleryBlock, self.getConfigs())


def detach_children_of(block: Element) -> list[Element]:
    children = list(block)
    for child in children:
        block.remove(child)
    return children


def ensure_first_is_heading(children: list[Element]) -> None:
    starts_with_heading = len(children) > 0 and is_heading(children[0])
    if not starts_with_heading:
        raise GalleryError(
            "Expected a gallery block to start with a heading that names its "
            "first section, but it does not."
        )


def is_heading(element: Element) -> bool:
    return element.tag in HEADINGS


def add_section_to(block: Element) -> None:
    SubElement(block, "section", {"slot": f"panel-{len(block)}"})


def add_to_last_section_of(block: Element, child: Element) -> None:
    block[-1].append(child)


def makeExtension() -> GalleryExtension:
    return GalleryExtension()
