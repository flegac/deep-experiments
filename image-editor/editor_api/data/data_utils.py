import numpy as np

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataSource, DataOperator, VariableSource, PipelineOperator


class EmptySource(DataSource):
    def get_buffer(self) -> Buffer:
        return np.zeros((10, 10, 3)).astype('uint8')


class RandomSource(DataSource):
    def get_buffer(self) -> Buffer:
        return (np.random.rand(128, 128, 3) * 255).astype('uint8')


class IdentityOperator(DataOperator):
    def apply(self, data: Buffer) -> Buffer:
        return data


class DataUtils:
    random_source = RandomSource()
    empty_source = EmptySource()
    identity = IdentityOperator()

    pipeline = PipelineOperator()

    @staticmethod
    def var_source(name: str) -> VariableSource:
        return VariableSource(name)
