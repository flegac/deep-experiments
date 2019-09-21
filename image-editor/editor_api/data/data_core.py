import abc
from typing import Callable, List, Union

from editor_api.data.buffer import Buffer


class DataSource(abc.ABC):
    def get_buffer(self) -> Buffer:
        raise NotImplementedError()

    def __or__(self, operator: 'DataOperator') -> 'DataSource':
        return _ComplexSource(operator, self)

    def __repr__(self):
        return self.__class__.__name__.replace('Source', '')


class DataOperator(object):
    def apply(self, data: Buffer) -> Buffer:
        raise NotImplementedError()

    def __or__(self, other: 'DataOperator') -> 'DataOperator':
        return PipelineOperator([self, other])

    def __repr__(self):
        return self.__class__.__name__.replace('Operator', '')


class _ComplexSource(DataSource):
    def __init__(self, operator: DataOperator, source: DataSource):
        if isinstance(source, _ComplexSource):
            operator = source._operator | operator
            source = source._source
        self._operator = operator
        self._source = source

    def get_buffer(self) -> Buffer:
        return self._operator.apply(self._source.get_buffer())


class VariableSource(DataSource):
    def __init__(self, name: str, value: Union[DataSource, Buffer] = None):
        self.name = name
        self.value: Union[DataSource, Buffer] = value

    def get_buffer(self) -> Buffer:
        if isinstance(self.value, Buffer):
            return self.value
        return self.value.get_buffer()

    def __repr__(self):
        return '{}={}'.format(self.name, self.value)


class DataMixer(Callable[[List[DataSource]], DataSource]):
    def apply(self, data: List[Buffer]) -> Buffer:
        raise NotImplementedError()

    def __call__(self, sources: List[DataSource]) -> DataSource:
        return _MixedSource(self.apply, sources)

    def __repr__(self):
        return str(type(self)).replace('Mixer', '')


class DataWorkflow(DataSource):
    def __init__(self, variables: List[VariableSource], workflow: DataSource):
        self.variables = variables
        self._workflow = workflow

    def configure(self, values: List[Union[DataSource, Buffer]]):
        assert len(values) == len(self.variables)
        for i, _ in enumerate(values):
            self.variables[i].value = _
        return self

    def get_buffer(self) -> Buffer:
        return self._workflow.get_buffer()

    def __repr__(self):
        return 'Workflow[{}]'.format(self._workflow)


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

    def apply(self, data: Buffer) -> Buffer:
        for _ in self._operators:
            data = _.apply(data)
        return data


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