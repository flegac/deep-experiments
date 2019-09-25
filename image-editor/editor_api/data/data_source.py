from abc import ABC
from typing import TypeVar, Generic, List, Any

import pandas as pd
from pandas import DataFrame

from editor_api.data.buffer import Buffer

T = TypeVar('T')


class DataSource(Generic[T], ABC):
    def get_data(self) -> T:
        raise NotImplementedError()

    def __repr__(self):
        return self.__class__.__name__.replace('Source', '')


class ImageSource(DataSource[Buffer], ABC):
    def get_data(self) -> Buffer:
        return self.get_buffer()

    def get_buffer(self) -> Buffer:
        raise NotImplementedError()


class TableSource(DataSource[DataFrame]):
    def __init__(self, columns: List[str]):
        self.columns = columns
        self._source = DataFrame(columns=columns)

    def get_data(self) -> DataFrame:
        return self.get_table()

    def get_table(self) -> DataFrame:
        return self._source

    def clear(self):
        self._source.drop(self._source.index, inplace=True)

    def save(self, path: str):
        self._source.to_csv(path, index=False)

    def load(self, path: str):
        self.replace(pd.read_csv(path))

    def replace(self, source: DataFrame):
        self.check_columns(source)
        self._source = source

    def check_columns(self, source: DataFrame):
        if list(source) != self.columns:
            raise ValueError('Bad table format : {}, expected : {}'.format(list(source), self.columns))

    def add_row(self, row: List[Any]):
        self._source = self._source.append(dict(zip(self.columns, row)), ignore_index=True)
