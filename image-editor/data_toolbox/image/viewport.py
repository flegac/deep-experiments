from math import ceil, floor
from typing import Callable, Tuple

import cv2
import numpy as np

from data_toolbox.data.data_mixer import Buffer
from data_toolbox.data.data_operator import DataOperator

ViewportProvider = Callable[[], Tuple[int, int]]


class ViewportOperator(DataOperator):
    def __init__(self, viewport_provider: ViewportProvider):
        self.viewport_provider = viewport_provider
        self.zoom_factor = 1.
        self.x = 0
        self.y = 0
        self.x_crop = None
        self.y_crop = None
        self.target = None

    def zoom(self, factor: float):
        self.zoom_factor *= factor

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def get_offset(self):
        return self.x, self.y

    def canvas_to_image_coords(self, x_target, y_target):
        x_source = x_target + self.x - self.x_crop / self.zoom_factor
        y_source = y_target + self.y - self.y_crop / self.zoom_factor
        return int(x_source), int(y_source)

    def apply(self, source: Buffer) -> Buffer:
        w_target, h_target = self._prepare_target(source.shape[2])
        h_source, w_source = source.shape[:2]

        self.zoom_factor = max(self.zoom_factor, min(w_target / w_source, h_target / h_source))

        w = min(w_source, ceil(w_target / self.zoom_factor))
        h = min(h_source, ceil(h_target / self.zoom_factor))

        self.x = min(max(self.x, 0), w_source - w)
        self.y = min(max(self.y, 0), h_source - h)

        w_crop = min(w_target, floor(w * self.zoom_factor))
        h_crop = min(h_target, floor(h * self.zoom_factor))

        self.x_crop = int((w_target - w_crop) / 2)
        self.y_crop = int((h_target - h_crop) / 2)

        crop_data = source[self.y:self.y + h, self.x:self.x + w]
        crop_data = cv2.resize(crop_data, (w_crop, h_crop))
        self.target[self.y_crop:self.y_crop + h_crop, self.x_crop:self.x_crop + w_crop] = crop_data
        return self.target

    def _prepare_target(self, bands: int):
        width, height = self.viewport_provider()

        if self.target is None or self.target.shape[:2] != (height, width):
            self.target = np.zeros((height, width, bands)).astype(np.uint8)
        else:
            self.target.fill(0)
        return width, height

    def __repr__(self) -> str:
        return 'Viewport[Z={}]({},{})'.format(self.zoom_factor, self.x, self.y)
