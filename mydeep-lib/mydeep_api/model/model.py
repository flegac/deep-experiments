import random
from abc import ABC

from mydeep_api.dataset.column import Column


class FitReport(object):
    pass


class FitConfig(object):
    def __init__(self, seed: float = random.random()):
        self.seed = seed


class Model(ABC):

    def fit(self, x: Column, y: Column, config: FitConfig = None) -> FitReport:
        raise NotImplementedError()

    def predict(self, x: Column) -> Column:
        raise NotImplementedError()
