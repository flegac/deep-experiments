from editor_api.data import Buffer

import numpy as np


def rasterio_to_opencv(data: Buffer) -> Buffer:
    data = np.moveaxis(data, 1, 2)
    data = np.moveaxis(data, 0, 2)
    return data


def opencv_to_rasterio(data: Buffer) -> Buffer:
    data = np.moveaxis(data, 1, 2)
    data = np.moveaxis(data, 0, 2)
    return data
