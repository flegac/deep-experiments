import cv2
import numpy as np

from editor_api.data import DataOperator, Buffer


class ErodeOperator(DataOperator):
    def apply(self, data: Buffer) -> Buffer:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(data, kernel, iterations=1)
