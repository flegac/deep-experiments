import os

import cv2
import itertools
import numpy as np
import pandas as pd
from typing import Iterator, List, Sized

from mydeep_api.tensor import Tensor


class Dataset(Sized):
    @property
    def x(self) -> Iterator[Tensor]:
        raise NotImplementedError()

    @property
    def y(self) -> Iterator[Tensor]:
        raise NotImplementedError()


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


class DirectoryDataset(Dataset):
    def __init__(self, x_path: str, y_path: str):
        self.x_path = x_path
        self.y_path = y_path

    @property
    def x(self) -> Iterator[Tensor]:
        for cat in os.listdir(self.x_path):
            for file in os.listdir(os.path.join(self.x_path, cat)):
                yield cv2.imread(os.path.join(self.x_path, cat, file))

    @property
    def y(self) -> Iterator[Tensor]:
        for cat in os.listdir(self.y_path):
            for file in os.listdir(os.path.join(self.y_path, cat)):
                yield cv2.imread(os.path.join(self.y_path, cat, file))


def test_numpy_dataset():
    x = np.random.rand(10, 2, 2)
    y = np.random.rand(10, 2, 2)

    db = NumpyDataset(x, y)

    for x in db.x:
        print(x.shape)


def test_directory_dataset():
    x = 'D:/Datasets/10-monkey-species/training'
    y = 'D:/Datasets/10-monkey-species/validation'

    db = DirectoryDataset(x_path=x,
                          y_path=y)

    for x in itertools.islice(db.x, 10):
        print(x.shape)


def test_pandas_dataset():
    csv = pd.read_csv('D:/Datasets/sign-language-mnist/sign_mnist_test.csv')
    db = PandasDataset(csv, col_x=['pixel1', 'pixel2', 'pixel3', 'pixel4', 'pixel5'], col_y=['label'])

    for x in itertools.islice(db.x, 10):
        print(x.shape)
