from math import ceil
from typing import Callable, Tuple

import cv2

from editor_api.data import Buffer, DataOperator

ViewportProvider = Callable[[], Tuple[int, int]]


class ViewportTransformer(DataOperator):
    def __init__(self, viewport_provider: ViewportProvider):
        self.viewport_provider = viewport_provider
        self.zoom_factor = 1.
        self.x = 0
        self.y = 0

    def zoom(self, factor: float):
        self.zoom_factor *= factor

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def get_offset(self):
        return self.x, self.y

    def __call__(self, data: Buffer) -> Buffer:
        width, height = self.viewport_provider()
        img_width = data.shape[1]
        img_height = data.shape[0]

        aspect = width / height

        self.zoom_factor = max(self.zoom_factor, width / img_width if aspect > 1 else height / img_height)

        w = min(img_width, ceil(width / self.zoom_factor))
        h = min(img_height, ceil(height / self.zoom_factor))

        self.x = min(max(self.x, 0), img_width - w)
        self.y = min(max(self.y, 0), img_height - h)

        crop_data = data[self.y:self.y + h, self.x:self.x + w]

        data = cv2.resize(crop_data, (width, height))
        return data

    def __repr__(self) -> str:
        return 'Viewport[Z={}]({},{})'.format(self.zoom_factor, self.x, self.y)
