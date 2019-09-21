import cv2
import numpy as np

from editor_api.data.data_core import Buffer
from editor_api.data.data_core import DataOperator


class ErodeOperator(DataOperator):
    def apply(self, data: Buffer) -> Buffer:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(data, kernel, iterations=1)
