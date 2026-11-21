from faran_visualizer import Array, Plot

from numpy.typing import ArrayLike
from jaxtyping import Float
from pytest import approx

import numpy as np


class plots:
    @staticmethod
    def has_line(plot: Plot, *, values: ArrayLike) -> bool:
        return any(line.values == approx(np.asarray(values)) for line in plot.lines)

    @staticmethod
    def bound_values(plot: Plot) -> Float[Array, " N"]:
        """Returns the values of every bound, sorted."""
        return np.sort(
            np.array(
                [value for bound in plot.bounds for value in np.ravel(bound.values)],
                dtype=float,
            )
        )
