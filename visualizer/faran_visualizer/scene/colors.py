from typing import Final, Sequence

from faran_visualizer.scene.animation import Color

NAMED_COLORS: Final = {
    "black": "#000000",
    "white": "#ffffff",
    "gray": "#808080",
    "grey": "#808080",
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "orange": "#ffa500",
    "purple": "#800080",
    "pink": "#ffc0cb",
    "brown": "#a52a2a",
    "cyan": "#00ffff",
    "magenta": "#ff00ff",
    "teal": "#008080",
    "navy": "#000080",
}


class InvalidColorError(ValueError):
    """Raised when a color is neither a hex color nor a supported color name."""


def color(value: str, *, alpha: float = 1.0) -> Color:
    """Parses `#rgb`, `#rrggbb`, `#rrggbbaa` or a basic color name.

    `alpha` multiplies the color's own alpha.

    Raises:
        InvalidColorError: If the color has another format.
    """
    digits = full_hex_digits(NAMED_COLORS.get(value.lower(), value), original=value)
    red, green, blue, own_alpha = (int(digits[i : i + 2], 16) for i in (0, 2, 4, 6))
    return Color(red=red, green=green, blue=blue, alpha=round(own_alpha * alpha))


def line_color(value: str | None, *, index: int, palette: Sequence[str]) -> Color:
    """Returns the given color, or the palette color for the line at `index`."""
    return color(value if value is not None else palette[index % len(palette)])


def full_hex_digits(value: str, *, original: str) -> str:
    digits = value.removeprefix("#")

    if not value.startswith("#") or not is_hex(digits):
        raise invalid_color(original)

    match len(digits):
        case 3:
            return "".join(digit * 2 for digit in digits) + "ff"
        case 6:
            return digits + "ff"
        case 8:
            return digits
        case _:
            raise invalid_color(original)


def is_hex(digits: str) -> bool:
    return all(digit in "0123456789abcdefABCDEF" for digit in digits)


def invalid_color(value: str) -> InvalidColorError:
    return InvalidColorError(
        f"Color '{value}' is not supported. Expected a hex color such as '#3498db' "
        f"or one of: {', '.join(NAMED_COLORS)}."
    )
