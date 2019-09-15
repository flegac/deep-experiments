import cv2
import numpy as np


class Viewport(object):
    def __init__(self, data: np.ndarray):
        self.data = data
        self.zoom_factor = 1.
        self.x = 0
        self.y = 0

    def zoom(self, factor: float):
        self.zoom_factor *= factor

    def move(self, dx: float, dy: float):
        self.x += dx
        self.y += dy

    def get_buffer(self, width: int, height: int):
        aspect = width / height

        img_width = self.data.shape[1]
        img_height = self.data.shape[0]

        self.zoom_factor = max(self.zoom_factor, max(width / img_width, height / img_height))

        w = min(img_width, int(width / self.zoom_factor))
        h = min(img_height, int(height / self.zoom_factor))
        if aspect > 1:
            h = int(w / aspect)
        else:
            w = int(h * aspect)

        self.x = min(max(self.x, 0), img_width - w)
        self.y = min(max(self.y, 0), img_height - h)

        return cv2.resize(self.data[self.y:self.y + h, self.x:self.x + w], (width, height))

    def __repr__(self) -> str:
        return 'Viewport[Z={}]({},{})'.format(self.zoom_factor, self.x, self.y)
