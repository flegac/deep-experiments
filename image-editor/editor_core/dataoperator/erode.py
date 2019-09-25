import cv2
import numpy as np

from editor_api.data.data_mixer import Buffer
from editor_api.data.data_operator import DataOperator


class ErodeOperator(DataOperator):
    def apply(self, source: Buffer) -> Buffer:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(source, kernel, iterations=1)
