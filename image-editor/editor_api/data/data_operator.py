from typing import List

from editor_api.data.buffer import Buffer
from editor_api.data.data_source import DataSource


class DataOperator(object):
    def apply(self, source: Buffer) -> Buffer:
        raise NotImplementedError()

    def as_source(self, source: DataSource) -> DataSource:
        return _ComplexSource(self, source)

    def __or__(self, other: 'DataOperator') -> 'DataOperator':
        return PipelineOperator([self, other])

    def __repr__(self):
        return self.__class__.__name__.replace('Operator', '')


class PipelineOperator(DataOperator):
    def __init__(self, operators: List[DataOperator] = None):
        self._operators = []
        if operators is not None:
            for step in operators:
                if step is None:
                    continue
                if isinstance(step, PipelineOperator):
                    self._operators.extend(step.pipeline)
                else:
                    self._operators.append(step)

    @property
    def pipeline(self):
        return self._operators

    def apply(self, source: Buffer) -> Buffer:
        for _ in self._operators:
            source = _.apply(source)
        return source


class _ComplexSource(DataSource):
    def __init__(self, operator: DataOperator, source: DataSource):
        if isinstance(source, _ComplexSource):
            operator = source._operator | operator
            source = source._source
        self._operator = operator
        self._source = source

    def get_buffer(self) -> Buffer:
        return self._operator.apply(self._source.get_buffer())
