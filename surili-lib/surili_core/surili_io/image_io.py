import abc

import cv2
import numpy as np


class ImageIO(abc.ABC):
    def read(self, path: str):
        raise NotImplementedError()

    def save(self, path: str, img: np.ndarray):
        raise NotImplementedError()


class OpencvIO(ImageIO):
    def read(self, path: str):
        return cv2.imread(path)

    def save(self, path: str, img: np.ndarray):
        cv2.imwrite(path, img)
        return path
