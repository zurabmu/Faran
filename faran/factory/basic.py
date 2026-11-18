from typing import Final

from faran.mppi import (
    NumPyMppi,
    NumPyZeroPadding,
    NoUpdate,
    UseOptimalControlUpdate,
    NoFilter,
    NumPySavGolFilter,
)
from faran.states import NumPyAugmentedMppi
from faran.mpcc import NumPyMpccMppi


class mppi:
    base: Final = NumPyMppi.create
    augmented: Final = NumPyAugmentedMppi.create
    mpcc: Final = NumPyMpccMppi.create


class update:
    none: Final = NoUpdate
    use_optimal_control: Final = UseOptimalControlUpdate


class padding:
    zero: Final = NumPyZeroPadding


class filters:
    none: Final = NoFilter
    savgol: Final = NumPySavGolFilter.create
