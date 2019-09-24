import cv2
import numpy as np

from editor_api.data.data_core import Buffer
from editor_api.data.data_core import DataOperator


class DilateOperator(DataOperator):
    def apply(self, source: Buffer) -> Buffer:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(source, kernel, iterations=1)
