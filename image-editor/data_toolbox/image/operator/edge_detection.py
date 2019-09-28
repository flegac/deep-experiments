import cv2
import numpy as np

from data_toolbox.data.data_mixer import Buffer
from data_toolbox.data.data_operator import DataOperator


class EdgeDetectionOperator(DataOperator):

    def apply(self, source: Buffer) -> Buffer:
        # data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        # data = cv2.bilateralFilter(data, 11, 17, 17)
        edged = cv2.Canny(source, 0, 255)
        return np.dstack((edged, edged, edged))
