from xml.etree.ElementTree import Element, SubElement

from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block, type_string


class ReplayError(Exception):
    """Raised when a replay block lacks a recording, a notebook or a code block."""


class ReplayBlock(Block):
    """A replay of a recorded example run, with the example's code in a panel.

    Write `/// replay | <caption>` around the example's code block. The option
    `recording` is the name of the recording file without its extension, and `notebook`
    is the name of the notebook that runs the example on Binder:

        /// replay | Obstacle avoidance
            recording: doc-static-obstacles
            notebook: 03_obstacle_avoidance

        ```python title="03_obstacle_avoidance.py"
        --8<-- "docs/examples/03_obstacle_avoidance.py"
        ```

        ///
    """

    NAME = "replay"
    ARGUMENT = True
    OPTIONS = {"recording": ("", type_string), "notebook": ("", type_string)}

    def on_create(self, parent: Element) -> Element:
        for option in ("recording", "notebook"):
            if self.options[option] == "":
                raise ReplayError(
                    f"Expected the replay '{self.argument}' to have the option "
                    f"'{option}', but it has none."
                )
        replay = SubElement(
            parent,
            "faran-replay",
            {
                "caption": self.argument,
                "recording": self.options["recording"],
                "notebook": self.options["notebook"],
            },
        )
        SubElement(replay, "div", {"slot": "source"})
        return replay

    def on_add(self, block: Element) -> Element:
        return block[0]

    def on_end(self, block: Element) -> None:
        if len(block[0]) == 0:
            raise ReplayError(
                f"Expected the replay '{self.argument}' to hold the example's code "
                "block, but it is empty."
            )


class ReplayExtension(BlocksExtension):
    """Adds the `/// replay` block."""

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(ReplayBlock, self.getConfigs())


def makeExtension() -> ReplayExtension:
    return ReplayExtension()
