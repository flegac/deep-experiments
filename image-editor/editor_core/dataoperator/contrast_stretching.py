import numpy as np
from skimage import exposure

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataOperator


class ContrastStretchingOperator(DataOperator):

    def apply(self, source: Buffer) -> Buffer:
        p2, p98 = np.percentile(source, (1, 99))
        return exposure.rescale_intensity(source, in_range=(p2, p98))
