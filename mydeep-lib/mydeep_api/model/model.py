from abc import ABC

from mydeep_api.dataset.dataset import Dataset


class FitReport(object):
    pass


class Model(ABC):
    def fit(self, x: Dataset, y: Dataset) -> FitReport:
        raise NotImplementedError()

    def predict(self, x: Dataset) -> Dataset:
        raise NotImplementedError()
