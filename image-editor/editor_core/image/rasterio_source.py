import os

import rasterio

from editor_api.data.data_mixer import Buffer
from editor_api.data.data_source import ImageSource
from editor_core.image.utils import rasterio_to_opencv


class RasterioSource(ImageSource):
    def __init__(self, path: str):
        self.path = path
        with rasterio.Env():
            with rasterio.open(self.path) as data:
                self.data = rasterio_to_opencv(data.get_data())
                # data.read(
                #     window=Window(*offset[::-1], *size),
                #     # out_shape=(self.data.height * 2, self.data.width * 2, self.data.count),
                #     # resampling=Resampling.bilinear
                # )

    def get_buffer(self) -> Buffer:
        return self.data

    def __repr__(self):
        return os.path.basename(self.path)
