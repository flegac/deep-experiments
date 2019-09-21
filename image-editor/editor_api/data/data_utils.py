from typing import Tuple

import numpy as np

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataSource, DataOperator, VariableSource, PipelineOperator


class EmptySource(DataSource):
    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        return np.zeros((1, 1, 3))


class IdentityOperator(DataOperator):
    def apply(self, data: Buffer) -> Buffer:
        return data


class DataUtils:
    empty_source = EmptySource()
    identity = IdentityOperator()

    pipeline = PipelineOperator()

    @staticmethod
    def var_source() -> VariableSource:
        return VariableSource()
