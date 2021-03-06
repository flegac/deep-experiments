from abc import ABC
from typing import Callable, List, Union

from data_toolbox.image.buffer import Buffer
from data_toolbox.image.source.buffer_source import BufferSource
from data_toolbox.data.data_source import DataSource
from data_toolbox.table.table import Table


class DataMixer(ABC):
    def apply(self, data: List[Union[Buffer, Table]]) -> Union[Buffer, Table]:
        raise NotImplementedError()

    def as_source(self, sources: List[DataSource]) -> DataSource:
        return _MixedBufferSource(self.apply, sources)

    def __repr__(self):
        return str(type(self)).replace('Mixer', '')


class _MixedSource(DataSource):
    def __init__(self, operator: Callable[[List[Buffer]], Buffer], sources: List[DataSource]):
        self._operator = operator
        self._sources = sources

    def get_data(self):
        buffers = [
            _.get_data()
            for _ in self._sources
        ]
        return self._operator(buffers)


class _MixedBufferSource(BufferSource):
    def __init__(self, operator: Callable[[List[Buffer]], Buffer], sources: List[DataSource]):
        self._operator = operator
        self._sources = sources

    def get_data(self):
        buffers = [
            _.get_data()
            for _ in self._sources
        ]
        return self._operator(buffers)

    def __repr__(self):
        return '[{}]'.format(['{:.4}'.format(str(_)) for _ in self._sources])
