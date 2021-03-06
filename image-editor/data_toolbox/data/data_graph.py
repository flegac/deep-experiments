from typing import Union, List, Any, Tuple

from data_toolbox.image.buffer import Buffer
from data_toolbox.data.data_mixer import DataMixer
from data_toolbox.data.data_operator import DataOperator
from data_toolbox.data.data_source import DataSource
from data_toolbox.image.buffer_factory import BufferSource

Node = Union[DataSource, Tuple[DataOperator, Any], Tuple[DataMixer, Any]]


def source(src: DataSource):
    return src


def mix(op: DataMixer, sources: List[Node]):
    return (op, sources)


def seq(op: DataOperator, source: Node):
    return (op, source)


def as_source(node: Node) -> DataSource:
    if isinstance(node, DataSource):
        return node
    op, sources = node

    if isinstance(op, DataMixer):
        return op.as_source([as_source(_) for _ in sources])

    if isinstance(op, DataOperator):
        return op.as_source(as_source(sources))

    raise ValueError('unsupported graph structure !')


class DataGraph:
    def __init__(self, variables: List[BufferSource], root_node: Node):
        self.variables = variables
        self._root = root_node

    def configure(self, values: List[Union[DataSource, Buffer]]):
        assert len(values) == len(self.variables)
        for i, _ in enumerate(values):
            self.variables[i].value = _
        return self

    def as_source(self):
        return as_source(self._root)

    def __repr__(self):
        return 'Workflow[{}]'.format(self._root)
