import numpy as np
from skimage import exposure

from editor.core.api.data_transformer import DataTransformer


class ContrastStretchingTransform(DataTransformer):

    def apply(self, data: np.ndarray) -> np.ndarray:
        p2, p98 = np.percentile(data, (1, 99))
        return exposure.rescale_intensity(data, in_range=(p2, p98))

