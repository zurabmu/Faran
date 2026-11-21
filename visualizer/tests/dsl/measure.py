from numpy.typing import ArrayLike

import numpy as np


class measure:
    @staticmethod
    def extent(strip: ArrayLike) -> tuple[float, float]:
        """Returns the width and height of the box around the points of a strip."""
        points = np.asarray(strip, dtype=float)
        width, height = points.max(axis=0) - points.min(axis=0)
        return float(width), float(height)

    @staticmethod
    def extent_along(strip: ArrayLike, *, direction: tuple[float, float]) -> float:
        """Returns how far the points of a strip spread along the direction."""
        unit = np.asarray(direction) / np.linalg.norm(direction)
        projections = np.asarray(strip, dtype=float) @ unit
        return float(projections.max() - projections.min())

    @staticmethod
    def center(strip: ArrayLike) -> tuple[float, float]:
        """Returns the center of the box around the points of a strip."""
        points = np.asarray(strip, dtype=float)
        x, y = (points.max(axis=0) + points.min(axis=0)) / 2
        return float(x), float(y)
