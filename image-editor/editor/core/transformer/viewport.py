from typing import Callable, Tuple

import cv2
import numpy as np

from editor.core.api.data_transformer import DataTransformer

ViewportProvider = Callable[[], Tuple[int, int]]


class ViewportTransform(DataTransformer):
    def __init__(self, viewport_provider: ViewportProvider):
        self.viewport_provider = viewport_provider
        self.zoom_factor = 1.
        self.x = 0
        self.y = 0
        self.with_contrast_stretching = False

        self.with_normalization = False

    def zoom(self, factor: float):
        self.zoom_factor *= factor

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def apply(self, data: np.ndarray) -> np.ndarray:

        width, height = self.viewport_provider()
        img_width = data.shape[1]
        img_height = data.shape[0]

        aspect = width / height
        img_aspect = img_width / img_height

        self.zoom_factor = max(self.zoom_factor, min(width / img_width, height / img_height))

        w = min(img_width, int(width / self.zoom_factor))
        h = min(img_height, int(height / self.zoom_factor))

        if aspect > 1:
            h = int(w / aspect)
        else:
            w = int(h * aspect)

        self.x = min(max(self.x, 0), img_width - w)
        self.y = min(max(self.y, 0), img_height - h)

        data = cv2.resize(data[self.y:self.y + h, self.x:self.x + w], (width, height))
        return data

    def __repr__(self) -> str:
        return 'Viewport[Z={}]({},{})'.format(self.zoom_factor, self.x, self.y)
