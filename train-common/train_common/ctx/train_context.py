from typing import Callable

from hyper_search.train_parameters import TrainParameters
from train_common.ctx.model import Model


class TrainContext:
    def __init__(self,
                 model_provider: Callable[[], Model],
                 params: TrainParameters,
                 augmentation):
        self.model_provider = model_provider
        self.params = params
        self.augmentation = augmentation

    @property
    def model(self):
        return self.model_provider()
