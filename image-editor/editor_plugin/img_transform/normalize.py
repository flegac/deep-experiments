import numpy as np

from editor.core.api.data_pipeline import DataTransform


class NormalizeTransform(DataTransform):

    def apply(self, data: np.ndarray) -> np.ndarray:
        data = data - data.min()
        data = 255 * (data / max(1, data.max()))
        return data.astype('uint8')
