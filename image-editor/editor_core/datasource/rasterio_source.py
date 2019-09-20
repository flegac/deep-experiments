import os
from typing import Tuple

import rasterio

from editor_api.data import DataSource, Buffer
from editor_core.utils import rasterio_to_opencv


class RasterioSource(DataSource):
    def __init__(self, path: str):
        self.path = path
        with rasterio.Env():
            with rasterio.open(self.path) as data:
                self.data = rasterio_to_opencv(data.get_buffer())
                # data.read(
                #     window=Window(*offset[::-1], *size),
                #     # out_shape=(self.data.height * 2, self.data.width * 2, self.data.count),
                #     # resampling=Resampling.bilinear
                # )

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        return self.data[offset[1]:offset[0], size[1]:size[0]]

    def __repr__(self):
        return os.path.basename(self.path)
