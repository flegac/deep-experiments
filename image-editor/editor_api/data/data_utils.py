from typing import Union

import numpy as np

from editor_api.data.buffer import Buffer
from editor_api.data.data_operator import DataOperator, PipelineOperator
from editor_api.data.data_source import DataSource


class EmptySource(DataSource):
    def get_buffer(self) -> Buffer:
        return np.zeros((10, 10, 3)).astype('uint8')


class RandomSource(DataSource):
    def get_buffer(self) -> Buffer:
        return (np.random.rand(128, 128, 3) * 255).astype('uint8')


class IdentityOperator(DataOperator):
    def apply(self, source: Buffer) -> Buffer:
        return source


class VariableSource(DataSource):
    def __init__(self, name: str, value: Union[DataSource, Buffer] = None):
        self.name = name
        self.value: Union[DataSource, Buffer] = value

    def get_buffer(self) -> Buffer:
        if isinstance(self.value, Buffer):
            return self.value
        return self.value.get_buffer()

    def __repr__(self):
        return '{}={}'.format(self.name, self.value)


class DataUtils:
    empty_source = EmptySource()
    random_source = RandomSource()

    identity = IdentityOperator()
    pipeline = PipelineOperator()

    @staticmethod
    def var_source(name: str) -> VariableSource:
        return VariableSource(name)
