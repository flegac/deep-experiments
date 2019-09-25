from typing import List

import numpy as np

from editor_api.data.data_mixer import Buffer, DataMixer
from editor_api.data.data_operator import DataOperator
from editor_api.data.data_graph import DataGraph, seq
from editor_api.data.data_utils import DataUtils


class Op(DataOperator):
    def apply(self, source: Buffer) -> Buffer:
        return source + 1


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
    b123 = (mix, [
        (op, (op, (op, s))),
        (op, (op, s)),
        (op, s)
    ])

    full = (op, (mix, [
        (op, (op, b123)),
        (op, (op, s))
    ]))

    graph = DataGraph(
        variables=[s],
        root_node=full
    )
    print()
    print(graph)
    print(graph.configure([np.zeros((3, 3))]).as_source().get_buffer())
