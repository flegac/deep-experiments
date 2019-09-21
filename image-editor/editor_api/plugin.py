import abc
from typing import List

from editor_api.data.data_core import DataOperator
from editor_api.process import DataProcessFactory


class Plugin(abc.ABC):
    def __init__(self):
        self._operators: List[DataOperator] = []
        self._processes: List[DataProcessFactory] = []

    def operators(self) -> List[DataOperator]:
        return self._operators

    def processes(self) -> List[DataProcessFactory]:
        return self._processes

    def extend(self, plugin: 'Plugin'):
        self._operators.extend(plugin.operators())
        self._processes.extend(plugin.processes())
