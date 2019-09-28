from typing import List

import numpy as np

from data_toolbox.data.data_mixer import Buffer, DataMixer
from data_toolbox.data.data_operator import DataOperator
from data_toolbox.data.data_graph import DataGraph
from data_toolbox.image.buffer_factory import ImageFactory


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
s = ImageFactory.variable('x')
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
    print(graph.configure([np.zeros((3, 3))]).as_source().get_data())
