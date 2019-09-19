from typing import Tuple, List

import numpy as np

from editor_api.data import DataSource, Buffer, DataOperator, DataMixer
from editor_api.data_workflow import DummySource, DataWorkflow


class DS(DataSource):
    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        return np.zeros(2, 2)


class Op(DataOperator):
    def apply(self, data: Buffer) -> Buffer:
        return data + 1


class Mix(DataMixer):
    def apply(self, data: List[Buffer]) -> Buffer:
        x = data[0]
        for y in data[1:]:
            x += y
        return x


# sources & operators
s = DummySource()
op1 = Op()
op2 = op1 | op1
op3 = op2 | op1
mix = Mix()


def test_complex_operators():
    b123 = mix([
        op2(s),
        op3(s),
        op1(s)
    ])
    graph = DataWorkflow(
        config=[s],
        workflow=mix([
            b123 | op2,
            op2(s)
        ]) | op1
    )
    print()
    print(graph.configure([np.zeros((3, 3))]).get_buffer(None, None))
