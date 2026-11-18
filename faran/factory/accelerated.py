from typing import Final

from faran.mppi import (
    JaxMppi,
    JaxZeroPadding,
    NoUpdate,
    UseOptimalControlUpdate,
    NoFilter,
    JaxSavGolFilter,
)
from faran.states import JaxAugmentedMppi
from faran.mpcc import JaxMpccMppi


class mppi:
    base: Final = JaxMppi.create
    augmented: Final = JaxAugmentedMppi.create
    mpcc: Final = JaxMpccMppi.create


class update:
    none: Final = NoUpdate
    use_optimal_control: Final = UseOptimalControlUpdate


class padding:
    zero: Final = JaxZeroPadding


class filters:
    none: Final = NoFilter
    savgol: Final = JaxSavGolFilter.create
