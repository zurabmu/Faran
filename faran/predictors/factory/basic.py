from typing import Final

from faran.predictors.common import StaticPredictor, CurvilinearPredictor


class predictor:
    curvilinear: Final = CurvilinearPredictor.create
    static: Final = StaticPredictor.create
