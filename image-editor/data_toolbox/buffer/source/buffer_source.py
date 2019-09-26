from abc import ABC

from data_toolbox.buffer.buffer import Buffer
from data_toolbox.data.data_source import DataSource


class BufferSource(DataSource[Buffer], ABC):
    def get_data(self) -> Buffer:
        return self.get_buffer()

    def get_buffer(self) -> Buffer:
        raise NotImplementedError()
