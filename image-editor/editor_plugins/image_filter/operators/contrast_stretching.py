import numpy as np
from skimage import exposure

from editor_api.data import DataOperator, Buffer


class ContrastStretchingOperator(DataOperator):

    def apply(self, data: Buffer) -> Buffer:
        p2, p98 = np.percentile(data, (1, 99))
        return exposure.rescale_intensity(data, in_range=(p2, p98))
