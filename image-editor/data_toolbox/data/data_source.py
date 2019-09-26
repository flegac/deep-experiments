from abc import ABC
from typing import TypeVar, Generic

T = TypeVar('T')


class DataSource(Generic[T], ABC):
    def get_data(self) -> T:
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__.replace('Source', '')
