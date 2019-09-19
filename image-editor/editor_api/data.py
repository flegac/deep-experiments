import abc
from typing import Callable, Tuple, List

import numpy as np

Buffer = np.ndarray


class DataSource(abc.ABC):

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        raise NotImplementedError()

    def __or__(self, operator: 'DataOperator') -> 'DataSource':
        return _ComplexSource(operator, self)

    def __repr__(self):
        return self.__class__.__name__.replace('Source', '')


class DataOperator(Callable[[DataSource], DataSource]):
    def apply(self, data: Buffer) -> Buffer:
        raise NotImplementedError()

    def __or__(self, other: 'DataOperator') -> 'DataOperator':
        return PipelineOperator([self, other])

    def __call__(self, source: DataSource) -> DataSource:
        return _ComplexSource(self, source)

    def __repr__(self):
        return self.__class__.__name__.replace('Operator', '')


class DataMixer(Callable[[List[DataSource]], DataSource]):
    def apply(self, data: List[Buffer]) -> Buffer:
        raise NotImplementedError()

    def __call__(self, sources: List[DataSource]) -> DataSource:
        return _MixedSource(self.apply, sources)

    def __repr__(self):
        return self.__class__.__name__.replace('Mixer', '')


class _ComplexSource(DataSource):
    def __init__(self, operator: DataOperator, source: DataSource):
        if isinstance(source, _ComplexSource):
            operator = source._operator | operator
            source = source._source
        self._operator = operator
        self._source = source

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        return self._operator.apply(self._source.get_buffer(offset, size))


class PipelineOperator(DataOperator):
    def __init__(self, operators: List[DataOperator] = None):
        self._operators = []
        if operators is not None:
            for _ in operators:
                self.add_transform(_)

    def apply(self, data: Buffer) -> Buffer:
        for _ in self._operators:
            data = _.apply(data)
        return data

    def add_transform(self, step: DataOperator):
        if step is not None:
            if isinstance(step, PipelineOperator):
                self._operators.extend(step._operators)
            else:
                self._operators.append(step)

    def clear(self):
        self._operators.clear()


class _MixedSource(DataSource):
    def __init__(self, operator: Callable[[List[Buffer]], Buffer], sources: List[DataSource]):
        self._operator = operator
        self._sources = sources

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]):
        buffers = [
            _.get_buffer(offset, size)
            for _ in self._sources
        ]
        return self._operator(buffers)
