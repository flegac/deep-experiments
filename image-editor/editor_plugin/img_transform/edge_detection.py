import cv2
import numpy as np

from editor.core.api.data_pipeline import DataTransform


class EdgeDetectionTransform(DataTransform):

    def apply(self, data: np.ndarray) -> np.ndarray:
        return cv2.Canny(data, 0, 255)
