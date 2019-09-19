import cv2
import numpy as np

from editor.core.data import DataTransformer, Buffer


class TileTransformer(DataTransformer):
    def __init__(self, tile_size: int = 128):
        self.tile_shape = (tile_size, tile_size)

    def __call__(self, data: Buffer) -> Buffer:
        h, w = data.shape[:2]
        n_x = int(w / self.tile_shape[0])
        n_y = int(h / self.tile_shape[1])
        x_split = np.array_split(np.arange(w), n_x)
        y_split = np.array_split(np.arange(h), n_y)

        for i in range(len(y_split)):
            for j in range(len(x_split)):
                p0 = (x_split[j][0], y_split[i][0])
                p1 = (x_split[j][- 1], y_split[i][- 1])
                cv2.rectangle(data, p0, p1, color=(0, 255, 0), thickness=1)

        # for _ in feature_extraction.image.extract_patches_2d(data, self.tile_shape):
        #     data = cv2.rectangle(data, (_[1], self.tile_shape[0]), (_[0], self.tile_shape[1]), color=(0, 255, 0))
        return data
