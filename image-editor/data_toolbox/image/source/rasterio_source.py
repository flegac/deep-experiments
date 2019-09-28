import os

import numpy as np
import rasterio

from data_toolbox.image.buffer import Buffer
from data_toolbox.image.source.buffer_source import BufferSource


class RasterioSource(BufferSource):
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


def rasterio_to_opencv(data: Buffer) -> Buffer:
    data = np.moveaxis(data, 1, 2)
    data = np.moveaxis(data, 0, 2)
    return data


def opencv_to_rasterio(data: Buffer) -> Buffer:
    data = np.moveaxis(data, 1, 2)
    data = np.moveaxis(data, 0, 2)
    return data
