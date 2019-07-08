from typing import List, Iterator, Tuple

import pandas as pd

from mydeep_api.dataset.dataset import Dataset
from mydeep_api.tensor import Tensor


class PandasDataset(Dataset):

    def __init__(self, dataframe: pd.DataFrame,
                 cols: List[str] = None):
        self.dataframe = dataframe
        self.cols = cols

    def __iter__(self) -> Iterator[Tensor]:
        for _ in self.dataframe[self.cols].to_numpy():
            yield _

    def __len__(self):
        return len(self.dataframe)

    @property
    def shape(self) -> Tuple[int, int, int]:
        return next(iter(self)).shape
