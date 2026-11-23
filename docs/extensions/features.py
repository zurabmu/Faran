from enum import StrEnum
from pathlib import Path
from typing import Any
from xml.etree.ElementTree import Element, SubElement

import msgspec
from markdown import Markdown
from pymdownx.blocks import BlocksExtension, BlocksProcessor
from pymdownx.blocks.block import Block


class Status(StrEnum):
    AVAILABLE = "available"
    PLANNED = "planned"


class FeatureLink(msgspec.Struct, frozen=True, forbid_unknown_fields=True):
    text: str
    href: str


class Feature(msgspec.Struct, frozen=True, forbid_unknown_fields=True):
    name: str
    status: Status
    description: str
    links: list[FeatureLink] = []


class Area(msgspec.Struct, frozen=True, forbid_unknown_fields=True):
    name: str
    features: list[Feature]


class FeaturesFile(msgspec.Struct, frozen=True, forbid_unknown_fields=True):
    areas: list[Area]


class FeaturesError(Exception):
    """Raised when the features file does not match the expected structure."""


class FeaturesBlock(Block):
    """The features of the library, one lane per area, read from the features file.

    Written as an empty `/// features` block. Each area becomes a level 2 heading followed by
    its features in order, available ones first. Links in the file are relative to the page
    that holds the block.
    """

    NAME = "features"

    def on_create(self, parent: Element) -> Element:
        container = SubElement(parent, "div", {"class": "faran-features"})
        for area in read_areas(Path(self.config["data_file"])):
            add_area(container, area)
        return container


class FeaturesExtension(BlocksExtension):
    """Adds the `/// features` block."""

    def __init__(self, **kwargs: Any) -> None:
        self.config = {
            "data_file": ["docs/features.yaml", "Path to the features file."]
        }
        super().__init__(**kwargs)

    def extendMarkdownBlocks(self, md: Markdown, block_mgr: BlocksProcessor) -> None:
        block_mgr.register(FeaturesBlock, self.getConfigs())


def read_areas(path: Path) -> list[Area]:
    try:
        return msgspec.yaml.decode(path.read_bytes(), type=FeaturesFile).areas
    except msgspec.ValidationError as error:
        raise FeaturesError(
            f"Expected the features file '{path}' to match the features structure, "
            f"but found: {error}."
        ) from error


def add_area(container: Element, area: Area) -> None:
    section = SubElement(container, "section", {"class": "faran-features__area"})
    SubElement(section, "h2").text = area.name
    lane = SubElement(section, "ol", {"class": "faran-features__lane"})
    for feature in in_status_order(area.features):
        add_feature(lane, feature)


def in_status_order(features: list[Feature]) -> list[Feature]:
    return sorted(features, key=lambda feature: list(Status).index(feature.status))


def add_feature(lane: Element, feature: Feature) -> None:
    item = SubElement(
        lane, "li", {"class": f"faran-feature faran-feature--{feature.status}"}
    )
    add_name(item, feature)
    add_description(item, feature)
    add_links(item, feature.links)


def add_name(item: Element, feature: Feature) -> None:
    name = SubElement(item, "p", {"class": "faran-feature__name"})
    name.text = feature.name
    is_planned = feature.status is Status.PLANNED
    if is_planned:
        SubElement(name, "span", {"class": "faran-feature__status"}).text = "Planned"


def add_description(item: Element, feature: Feature) -> None:
    description = SubElement(item, "p", {"class": "faran-feature__description"})
    description.text = feature.description


def add_links(item: Element, links: list[FeatureLink]) -> None:
    if not links:
        return
    paragraph = SubElement(item, "p", {"class": "faran-feature__links"})
    for link in links:
        SubElement(paragraph, "a", {"href": link.href}).text = link.text


def makeExtension(**kwargs: Any) -> FeaturesExtension:
    return FeaturesExtension(**kwargs)
