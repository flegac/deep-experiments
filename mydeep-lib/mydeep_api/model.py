from typing import Dict

from mydeep_api.tensor import Tensor


class FitReport(object):
    pass


class Model(object):
    def fit(self, x: Tensor, y: Tensor, config: Dict = None) -> FitReport:
        raise NotImplementedError()

    def predict(self, x: Tensor) -> Tensor:
        raise NotImplementedError()
