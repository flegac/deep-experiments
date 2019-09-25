from typing import Callable, List

from editor_api.data.buffer import Buffer
from editor_api.data.data_source import DataSource


class DataMixer(object):
    def apply(self, data: List[Buffer]) -> Buffer:
        raise NotImplementedError()

    def as_source(self, sources: List[DataSource]) -> DataSource:
        return _MixedSource(self.apply, sources)

    def __repr__(self):
        return str(type(self)).replace('Mixer', '')


class _MixedSource(DataSource):
    def __init__(self, operator: Callable[[List[Buffer]], Buffer], sources: List[DataSource]):
        self._operator = operator
        self._sources = sources

    def get_buffer(self):
        buffers = [
            _.get_buffer()
            for _ in self._sources
        ]
        return self._operator(buffers)
