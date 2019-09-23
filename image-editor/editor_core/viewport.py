from math import ceil, floor
from typing import Callable, Tuple

import cv2
import numpy as np

from editor_api.data.data_core import Buffer, DataOperator

ViewportProvider = Callable[[], Tuple[int, int]]


class ViewportOperator(DataOperator):
    def __init__(self, viewport_provider: ViewportProvider):
        self.viewport_provider = viewport_provider
        self.zoom_factor = 1.
        self.x = 0
        self.y = 0
        self.output_buffer = None

    def zoom(self, factor: float):
        self.zoom_factor *= factor

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def get_offset(self):
        return self.x, self.y

    def apply(self, data: Buffer) -> Buffer:
        w_target, h_target = self.viewport_provider()
        if self.output_buffer is None or self.output_buffer.shape[:2] != (h_target, w_target):
            self.output_buffer = np.zeros((h_target, w_target, data.shape[2])).astype('uint8')
        else:
            self.output_buffer.fill(0)

        w_source = data.shape[1]
        h_source = data.shape[0]

        self.zoom_factor = max(self.zoom_factor, min(w_target / w_source, h_target / h_source))

        w = min(w_source, ceil(w_target / self.zoom_factor))
        h = min(h_source, ceil(h_target / self.zoom_factor))

        self.x = min(max(self.x, 0), w_source - w)
        self.y = min(max(self.y, 0), h_source - h)

        crop_data = data[self.y:self.y + h, self.x:self.x + w]

        ww = min(w_target, floor(w * self.zoom_factor))
        hh = min(h_target, floor(h * self.zoom_factor))
        crop_data = cv2.resize(crop_data, (ww, hh))

        x = int((w_target - ww) / 2)
        y = int((h_target - hh) / 2)

        self.output_buffer[y:y + crop_data.shape[0], x:x + crop_data.shape[1]] = crop_data

        return self.output_buffer

    def __repr__(self) -> str:
        return 'Viewport[Z={}]({},{})'.format(self.zoom_factor, self.x, self.y)
