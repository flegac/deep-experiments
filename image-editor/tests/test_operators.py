from typing import List

import numpy as np

from editor_api.data.data_core import Buffer, DataOperator, DataMixer
from editor_api.data.data_core import DataWorkflow
from editor_api.data.data_utils import DataUtils


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
s = DataUtils.var_source('x')
op = Op()
mix = Mix()


def test_complex_operators():
    b123 = mix([
        s | (op | op | op),
        s | (op | op | op),
        s | op
    ])
    workflow = mix([
        b123 | op | op,
        s | (op | op)
    ]) | op

    graph = DataWorkflow(
        variables=[s],
        workflow=workflow
    )
    print()
    print(graph)
    print(graph.configure([np.zeros((3, 3))]).get_buffer())
