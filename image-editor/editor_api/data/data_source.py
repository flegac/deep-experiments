import abc

from editor_api.data.buffer import Buffer


class DataSource(abc.ABC):
    def get_buffer(self) -> Buffer:
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__.replace('Source', '')
