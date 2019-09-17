import abc

import numpy as np


class DataSource(abc.ABC):
    def get_buffer(self) -> np.ndarray:
        raise NotImplementedError()
