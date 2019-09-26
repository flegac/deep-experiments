import numpy as np
from skimage import exposure

from data_toolbox.buffer.buffer import Buffer
from data_toolbox.data.data_operator import DataOperator


class ContrastStretchingOperator(DataOperator):

    def apply(self, source: Buffer) -> Buffer:
        p2, p98 = np.percentile(source, (1, 99))
        return exposure.rescale_intensity(source, in_range=(p2, p98))
