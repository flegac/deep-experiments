from typing import Iterator

from mydeep_api.dataset import Dataset
from mydeep_api.tensor import Tensor


class NumpyDataset(Dataset):
    def __init__(self, x: Tensor, y: Tensor):
        self._x = x
        self._y = y

    @property
    def x(self) -> Iterator[Tensor]:
        return self._x

    @property
    def y(self) -> Iterator[Tensor]:
        return self._y

    def __len__(self):
        return len(self._x)
