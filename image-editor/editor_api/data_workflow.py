from typing import Tuple, List, Union

from editor_api.data import DataSource, Buffer


class DummySource(DataSource):
    def __init__(self, value: Union[DataSource, Buffer] = None):
        self.value: Union[DataSource, Buffer] = value

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        if isinstance(self.value, Buffer):
            return self.value
        return self.value.get_buffer(offset, size)


class DataWorkflow(DataSource):
    def __init__(self, config: List[DummySource], workflow: DataSource):
        self.config = config
        self._workflow = workflow

    def configure(self, values: List[Union[DataSource, Buffer]]):
        for i, _ in enumerate(values):
            self.config[i].value = _
        return self

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        return self._workflow.get_buffer(offset, size)
