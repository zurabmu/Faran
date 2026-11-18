from typing import Final

from faran.samplers.gaussian import NumPyGaussianSampler
from faran.samplers.halton import NumPyHaltonSplineSampler


class sampler:
    gaussian: Final = NumPyGaussianSampler.create
    halton: Final = NumPyHaltonSplineSampler.create
