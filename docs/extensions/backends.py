from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block

BACKENDS = ("NumPy", "JAX")


class BackendsError(Exception):
    """Raised when a backends block does not hold one part per backend."""


class BackendsBlock(Block):
    """A class of the API reference in each backend, with a tab per backend.

    Write `/// backends` around the `:::` block of the NumPy class followed by the one
    of the JAX class:

        /// backends

        ::: faran.mppi.savgol.basic.NumPySavGolFilter

        ::: faran.mppi.savgol.accelerated.JaxSavGolFilter

        ///
    """

    NAME = "backends"

    def on_markdown(self) -> str:
        return "block"

    def on_create(self, parent: Element) -> Element:
        return SubElement(parent, "faran-backends")

    def on_end(self, block: Element) -> None:
        if len(block) != len(BACKENDS):
            raise BackendsError(
                f"Expected a backends block to hold one part for each of {', '.join(BACKENDS)}, "
                f"but it holds {len(block)} parts."
            )
        parts = list(block)
        for backend, part in zip(BACKENDS, parts, strict=True):
            block.remove(part)
            SubElement(block, "div", {"slot": backend}).append(part)


class BackendsExtension(BlocksExtension):
    """Adds the `/// backends` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(BackendsBlock, self.getConfigs())


def makeExtension() -> BackendsExtension:
    return BackendsExtension()
