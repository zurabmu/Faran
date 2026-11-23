from html import escape
from importlib.resources import files
from importlib.resources.abc import Traversable
from string import Template


class EngineMissingError(Exception):
    """Raised when the canvas engine bundle is not in the installed package."""


def page_html(animation_json: str, *, title: str) -> str:
    """Returns a standalone HTML page that plays the animation with the canvas engine."""
    return Template(resource("page.html").read_text(encoding="utf-8")).substitute(
        title=escape(title),
        engine=engine_bundle(),
        animation=script_safe(animation_json),
    )


def engine_bundle() -> str:
    bundle = resource("engine.js")
    if not bundle.is_file():
        raise EngineMissingError(
            f"The canvas engine bundle {bundle} is missing. "
            "Build it with `just visualizer-engine`."
        )
    return bundle.read_text(encoding="utf-8")


def resource(name: str) -> Traversable:
    return files(__name__) / name


def script_safe(text: str) -> str:
    # NOTE: A "</" inside a script element would end it early.
    return text.replace("</", r"<\/")
