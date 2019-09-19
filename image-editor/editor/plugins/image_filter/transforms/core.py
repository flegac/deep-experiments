import cv2
import numpy as np

from editor.core.data import DataTransformer, Buffer


class DilateTransformer(DataTransformer):
    def __call__(self, data: Buffer) -> Buffer:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(data, kernel, iterations=1)


class ErodeTransformer(DataTransformer):
    def __call__(self, data: Buffer) -> Buffer:
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(data, kernel, iterations=1)
