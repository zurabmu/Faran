from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block, type_string


class VariantsError(Exception):
    """Raised when a variants block holds no variant or a variant is outside one."""


class VariantsBlock(Block):
    """Content that exists in several variants, of which the reader sees one at a time.

    Write `/// variants | <label>` around one `//// variant | <name>` block per variant.
    The label names the choice between the variants. Variants blocks with the same label
    on a page show the same variant:

        /// variants | Backend

        //// variant | NumPy
            note: Prototyping and debugging

        Content shown for NumPy.

        ////

        //// variant | JAX

        Content shown for JAX.

        ////

        ///
    """

    NAME = "variants"
    ARGUMENT = True

    def on_markdown(self) -> str:
        return "block"

    def on_create(self, parent: Element) -> Element:
        return SubElement(parent, "faran-variants", {"label": self.argument})

    def on_end(self, block: Element) -> None:
        if len(block) == 0:
            raise VariantsError(
                f"Expected the variants block '{self.argument}' to hold at least one "
                "'variant' block, but it holds none."
            )


class VariantBlock(Block):
    """One variant inside a variants block.

    Write `//// variant | <name>` inside a variants block, described in `VariantsBlock`.
    The option `note` is a short description shown with the name.
    """

    NAME = "variant"
    ARGUMENT = True
    OPTIONS = {"note": ("", type_string)}

    def on_create(self, parent: Element) -> Element:
        if parent.tag != "faran-variants":
            raise VariantsError(
                f"Expected the variant '{self.argument}' to be inside a variants block, "
                f"but it is inside <{parent.tag}>."
            )
        return SubElement(
            parent,
            "div",
            {
                "slot": f"variant-{len(parent)}",
                "data-name": self.argument,
                "data-note": self.options["note"],
            },
        )


class VariantsExtension(BlocksExtension):
    """Adds the `/// variants` and `/// variant` blocks."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(VariantsBlock, self.getConfigs())
        block_mgr.register(VariantBlock, self.getConfigs())


def makeExtension() -> VariantsExtension:
    return VariantsExtension()
