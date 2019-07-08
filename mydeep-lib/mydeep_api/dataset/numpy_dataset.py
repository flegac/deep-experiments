from typing import Iterator, Tuple

from mydeep_api.dataset.dataset import Dataset
from mydeep_api.tensor import Tensor


class NumpyDataset(Dataset):

    def __init__(self, data: Tensor):
        self._data = data

    def __iter__(self) -> Iterator[Tensor]:
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    @property
    def shape(self) -> Tuple[int, int, int]:
        return self._data[0].shape
