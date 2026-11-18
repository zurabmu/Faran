from typing import Final

from faran.samplers.gaussian import JaxGaussianSampler
from faran.samplers.halton import JaxHaltonSplineSampler


class sampler:
    gaussian: Final = JaxGaussianSampler.create
    halton: Final = JaxHaltonSplineSampler.create
