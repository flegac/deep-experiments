import itertools

import numpy as np
import pandas as pd

from mydeep_api.file_tree_dataset import FileTreeDataset
from mydeep_api.numpy_dataset import NumpyDataset
from mydeep_api.pandas_dataset import PandasDataset


def test_numpy_dataset():
    x = np.random.rand(10, 2, 2)
    y = np.random.rand(10, 2, 2)

    db = NumpyDataset(x, y)

    for x in db.x:
        print(x.shape)


def test_directory_dataset():
    x = 'D:/Datasets/10-monkey-species/training'
    y = 'D:/Datasets/10-monkey-species/validation'

    db = FileTreeDataset(x_path=x,
                         y_path=y)

    for x in itertools.islice(db.x, 10):
        print(x.shape)


def test_pandas_dataset():
    csv = pd.read_csv('D:/Datasets/sign-language-mnist/sign_mnist_test.csv')
    db = PandasDataset(csv, col_x=['pixel1', 'pixel2', 'pixel3', 'pixel4', 'pixel5'], col_y=['label'])

    for x in itertools.islice(db.x, 10):
        print(x.shape)