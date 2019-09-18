import numpy as np
from skimage import exposure

from editor.api.data import DataTransformer, Buffer


class NormalizeTransform(DataTransformer):

    def __call__(self, data: Buffer) -> Buffer:
        data = data - data.min()
        data = 255 * (data / max(1, data.max()))
        return data.astype('uint8')


class ContrastStretchingTransform(DataTransformer):

    def __call__(self, data: Buffer) -> Buffer:
        p2, p98 = np.percentile(data, (1, 99))
        return exposure.rescale_intensity(data, in_range=(p2, p98))
