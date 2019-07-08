import pandas as pd
from typing import List, Iterator

from mydeep_api.dataset import Dataset
from mydeep_api.tensor import Tensor


class PandasDataset(Dataset):
    def __init__(self, dataframe: pd.DataFrame,
                 col_x: List[str] = None,
                 col_y: List[str] = None):
        self.dataframe = dataframe
        self.col_x = col_x or ['x']
        self.col_y = col_y or ['y']

    @property
    def x(self) -> Iterator[Tensor]:
        for _ in self.dataframe[self.col_x].to_numpy():
            yield _

    @property
    def y(self) -> Iterator[Tensor]:
        for _ in self.dataframe[self.col_y].to_numpy():
            yield _

    def __len__(self):
        return len(self.dataframe)
