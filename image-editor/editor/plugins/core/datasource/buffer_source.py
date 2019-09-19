import numpy as np

from editor.core.data import DataSource, Buffer


class BufferSource(DataSource):
    def __init__(self, name: str, data: np.ndarray):
        self.name = name
        self.data = data

    def __call__(self) -> Buffer:
        return self.data
