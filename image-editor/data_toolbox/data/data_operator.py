from typing import List, Any

from data_toolbox.data.data_source import DataSource
from data_toolbox.image.buffer import Buffer


class DataOperator(object):
    def apply(self, source: DataSource) -> Any:
        raise NotImplementedError()

    def as_source(self, source: DataSource) -> DataSource:
        return _TransformedSource(self, source)

    def __or__(self, other: 'DataOperator') -> 'DataOperator':
        return PipeOperator([self, other])

    def __repr__(self):
        return self.__class__.__name__.replace('Operator', '')


class PipeOperator(DataOperator):
    def __init__(self, operators: List[DataOperator] = None):
        self._operators = []
        if operators is not None:
            for step in operators:
                if step is None:
                    continue
                if isinstance(step, PipeOperator):
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


class _TransformedSource(DataSource):
    def __init__(self, operator: DataOperator, source: DataSource):
        if isinstance(source, _TransformedSource):
            operator = source._operator | operator
            source = source._source
        self._operator = operator
        self._source = source

    def get_data(self) -> Buffer:
        return self._operator.apply(self._source.get_data())
