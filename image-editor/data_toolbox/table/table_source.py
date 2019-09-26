from typing import List, Any

import pandas as pd

from data_toolbox.data.data_source import DataSource
from data_toolbox.table.table import Table


class TableSource(DataSource[Table]):
    def __init__(self, columns: List[str] = None):
        self.columns = columns
        self._source = Table(columns=columns)

    def get_data(self) -> Table:
        return self.get_table()

    def get_table(self) -> Table:
        return self._source

    def clear(self):
        self._source.drop(self._source.index, inplace=True)
        return self

    def save(self, path: str):
        self._source.to_csv(path, index=False)

    def load(self, path: str):
        self.replace(pd.read_csv(path))
        return self

    def replace(self, source: Table):
        self.check_columns(source)
        self._source = source
        return self

    def check_columns(self, source: Table):
        if self.columns is not None and list(source) != self.columns:
            raise ValueError('Bad table format : {}, expected : {}'.format(list(source), self.columns))

    def add_row(self, row: List[Any]):
        self._source = self._source.append(dict(zip(self.columns, row)), ignore_index=True)
        return self
