from faran_visualizer.array import Array
from faran_visualizer.scene import Chart

from jaxtyping import Float

import numpy as np


def plotted_values(values: Float[Array, " N"], *, chart: Chart) -> Float[Array, " N"]:
    # NOTE: The plots of the viewer have no log axis, so log scales plot log10 values.
    match chart.scale:
        case "linear":
            return values
        case "log":
            return np.log10(values)


def axis_label(chart: Chart) -> str:
    match chart.scale:
        case "linear":
            return chart.y_label
        case "log":
            return f"log10 {chart.y_label}"
