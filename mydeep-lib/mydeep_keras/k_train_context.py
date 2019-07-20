from typing import Callable

from hyper_search.train_parameters import TrainParameters
from mydeep_keras.k_model import KModel


class KTrainContext(object):

    def __init__(self,
                 model_provider: Callable[[], KModel],
                 params: TrainParameters,
                 augmentation) -> None:
        super().__init__()
        self.model_provider = model_provider
        self.params = params
        self.augmentation = augmentation

    @property
    def model(self):
        return self.model_provider()
