import os

import rasterio

from editor_api.data.data_core import DataSource, Buffer
from editor_core.datasource.utils import rasterio_to_opencv


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

    def get_buffer(self) -> Buffer:
        return self.data

    def __repr__(self):
        return os.path.basename(self.path)
