import cv2
import numpy as np
from skimage import exposure


class Viewport(object):
    def __init__(self):
        self.data = np.zeros((10, 10, 3))
        self.zoom_factor = 1.
        self.x = 0
        self.y = 0
        self.with_contrast_stretching = False

        self.with_normalization = False

    def open(self, path: str):
        data = cv2.imread(path)
        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        self.data = data

    def zoom(self, factor: float):
        if self.data is None:
            return
        self.zoom_factor *= factor

    def move(self, dx: float, dy: float):
        if self.data is None:
            return
        self.x += dx
        self.y += dy

    def get_buffer(self, width: int, height: int):
        if self.data is None:
            return None

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

        data = cv2.resize(self.data[self.y:self.y + h, self.x:self.x + w], (width, height))
        data = self.image_transformation(data)
        return data

    def image_transformation(self, data: np.ndarray):
        # normalize image
        # TODO : normalize by band ??
        data = data - data.min()
        data = 255 * (data / max(1, data.max()))
        data = data.astype('uint8')

        if self.with_contrast_stretching:
            p2, p98 = np.percentile(data, (1, 99))
            data = exposure.rescale_intensity(data, in_range=(p2, p98))

        return data

    def __repr__(self) -> str:
        return 'Viewport[Z={}]({},{})'.format(self.zoom_factor, self.x, self.y)
