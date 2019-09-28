from typing import Union

import numpy as np

from data_toolbox.image.source.opencv_source import OpencvSource
from data_toolbox.image.source.rasterio_source import RasterioSource
from data_toolbox.data.data_operator import DataOperator, PipeOperator
from data_toolbox.image.buffer import Buffer
from data_toolbox.image.source.buffer_source import BufferSource


class BufferVariableSource(BufferSource):
    def __init__(self, name: str, value: Union[BufferSource, Buffer] = None):
        self.name = name
        self.value: Union[BufferSource, Buffer] = value

    def get_buffer(self) -> Buffer:
        if isinstance(self.value, Buffer):
            return self.value
        return self.value.get_data()

    def __repr__(self):
        return '{}={}'.format(self.name, self.value)


class EmptySource(BufferSource):
    def get_buffer(self) -> Buffer:
        return np.zeros((10, 10, 3)).astype('uint8')


class RandomSource(BufferSource):
    def get_buffer(self) -> Buffer:
        return (np.random.rand(128, 128, 3) * 255).astype('uint8')


class IdentityOperator(DataOperator):
    def apply(self, source: Buffer) -> Buffer:
        return source


class ImageFactory:
    empty = EmptySource()
    random = RandomSource()

    identity = IdentityOperator()
    pipeline = PipeOperator()

    @staticmethod
    def variable(name: str) -> BufferSource:
        return BufferVariableSource(name)

    @staticmethod
    def from_gray(path: str):
        return OpencvSource.from_gray(path)

    @staticmethod
    def from_rgb(path: str):
        return OpencvSource.from_rgb(path)
        # return RasterioSource(path)

    @staticmethod
    def from_rio(path: str):
        return RasterioSource(path)
