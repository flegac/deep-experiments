import numpy as np

from editor.core.api.data_transformer import DataTransformer


class NormalizeTransform(DataTransformer):

    def apply(self, data: np.ndarray) -> np.ndarray:
        data = data - data.min()
        data = 255 * (data / max(1, data.max()))
        return data.astype('uint8')
