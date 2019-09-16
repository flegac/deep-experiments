import numpy as np

from editor.core.api.data_pipeline import DataProvider


class Band(DataProvider):
    def __init__(self, name: str, data: np.ndarray, index: int):
        assert index < data.shape[2]
        self.name = name
        self.index = index
        self.data = data
        self.is_active = True

    def get_buffer(self):
        return self.data[:, :, self.index] if self.is_active else np.zeros(self.data.shape[:2])
