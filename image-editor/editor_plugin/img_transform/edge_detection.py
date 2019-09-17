import cv2
import numpy as np

from editor.core.api.data_transformer import DataTransformer


class EdgeDetectionTransform(DataTransformer):

    def apply(self, data: np.ndarray) -> np.ndarray:
        return cv2.Canny(data, 0, 255)
