from typing import Final


from faran.obstacles.provider import (
    JaxPredictingObstacleStateProvider,
)
from faran.obstacles.static import (
    JaxStaticObstacleSimulator,
)
from faran.obstacles.dynamic import (
    JaxDynamicObstacleSimulator,
)
from faran.obstacles.sampler import (
    JaxGaussianObstacle2dPoseSampler,
)
from faran.obstacles.assignment import (
    JaxHungarianObstacleIdAssignment,
)
from faran.obstacles.observer import NoisyObstacleStateObserver


class obstacles:
    empty: Final = JaxStaticObstacleSimulator.empty
    static: Final = JaxStaticObstacleSimulator.create
    dynamic: Final = JaxDynamicObstacleSimulator.create

    class provider:
        predicting: Final = JaxPredictingObstacleStateProvider.create

    class sampler:
        gaussian: Final = JaxGaussianObstacle2dPoseSampler.create

    class id_assignment:
        hungarian: Final = JaxHungarianObstacleIdAssignment.create

    class observer:
        noisy: Final = NoisyObstacleStateObserver.decorate
