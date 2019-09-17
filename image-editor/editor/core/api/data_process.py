import abc

import numpy as np


class DataProcess(abc.ABC):
    def compute(self, data: np.ndarray) -> None:
        raise NotImplementedError()

    def progress(self) -> float:
        raise NotImplementedError()
