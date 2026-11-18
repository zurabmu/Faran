from typing import Final


from faran.obstacles.provider import (
    PredictingObstacleStateProvider,
)
from faran.obstacles.static import (
    NumPyStaticObstacleSimulator,
)
from faran.obstacles.dynamic import (
    NumPyDynamicObstacleSimulator,
)
from faran.obstacles.sampler import (
    NumPyGaussianObstacle2dPoseSampler,
)
from faran.obstacles.assignment import (
    NumPyHungarianObstacleIdAssignment,
)
from faran.obstacles.observer import NoisyObstacleStateObserver


class obstacles:
    empty: Final = NumPyStaticObstacleSimulator.empty
    static: Final = NumPyStaticObstacleSimulator.create
    dynamic: Final = NumPyDynamicObstacleSimulator.create

    class provider:
        predicting: Final = PredictingObstacleStateProvider.create

    class sampler:
        gaussian: Final = NumPyGaussianObstacle2dPoseSampler.create

    class id_assignment:
        hungarian: Final = NumPyHungarianObstacleIdAssignment.create

    class observer:
        noisy: Final = NoisyObstacleStateObserver.decorate
