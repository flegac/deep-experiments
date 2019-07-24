import random
from abc import ABC

from mydeep_api.dataset.dataset import Dataset
from mydeep_api.dataset.bi_dataset import BiDataset


class FitReport(object):
    pass


class FitConfig(object):
    def __init__(self, seed: float = random.random()):
        self.seed = seed


class Model(ABC):

    def fit(self, dataset: BiDataset, config: FitConfig = None) -> FitReport:
        raise NotImplementedError()

    def predict(self, x: Dataset) -> Dataset:
        raise NotImplementedError()
