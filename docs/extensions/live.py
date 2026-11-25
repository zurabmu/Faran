from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block, type_boolean


class LiveBlock(Block):
    """A live snippet: a code block that readers can edit and run in the browser.

    Write `/// live | <caption>` around one code block. Add the option `still: true`
    when the code draws a single frame, so that the preview has no playback controls:

        /// live | Gaussian rollouts
            still: true

        ```python
        --8<-- "docs/snippets/gaussian.py"
        ```

        ///
    """

    NAME = "live"
    ARGUMENT = True
    OPTIONS = {"still": (False, type_boolean)}

    def on_markdown(self) -> str:
        return "block"

    def on_create(self, parent: Element) -> Element:
        attributes = {"caption": self.argument}
        if self.options["still"]:
            attributes["still"] = ""
        return SubElement(parent, "faran-live", attributes)


class LiveExtension(BlocksExtension):
    """Adds the `/// live` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(LiveBlock, self.getConfigs())


def makeExtension() -> LiveExtension:
    return LiveExtension()
