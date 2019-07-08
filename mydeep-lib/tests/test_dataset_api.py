import itertools
import shutil

import numpy as np

from mydeep_api.api import Data
from mydeep_api.dataset.numpy_dataset import NumpyDataset


def test_numpy_dataset():
    x = np.arange(40).reshape((10, 2, 2))
    y = np.arange(20).reshape((10, 2))

    db = Data.from_xy(x, y)

    print('is_segmentation={}'.format(db.is_segmentation))

    for x, y in itertools.islice(db, 5):
        print('shape: x={}, y={}'.format(x.shape, y.shape))


def test_from_folder_tree():
    db = Data.from_folder_tree(
        x_path='resources/dataset/folder_tree',
        x_shape=(256, 256),
        y_path='resources/dataset/folder_tree',
        y_shape=(256, 256)
    )
    print('is_segmentation={}'.format(db.is_segmentation))

    for x, y in itertools.islice(db, 5):
        print('shape: x={}, y={}'.format(x.shape, y.shape))


def test_from_csv():
    path = 'resources/dataset/dataset.csv'
    db = Data.from_csv(
        path,
        x_col=['x0', 'x1'],
        y_col=['y']
    )
    print('is_segmentation={}'.format(db.is_segmentation))

    for x, y in itertools.islice(db, 5):
        print('shape: x={}, y={}'.format(x.shape, y.shape))


def test_export_import():
    db = Data.from_xy(
        x=NumpyDataset(np.arange(60).reshape((5, 2, 2, 3))),
        y=NumpyDataset(np.arange(60).reshape((5, 2, 2, 3)))
    )
    out_path = '/tmp/test_export'
    shutil.rmtree(out_path, ignore_errors=True)

    db.export(out_path)
    db2 = Data.from_export(out_path)
    print('is_segmentation={}'.format(db2.is_segmentation))
    for x, y in db2:
        print('shape: x={}, y={}'.format(x.shape, y.shape))
    shutil.rmtree(out_path)
