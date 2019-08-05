import os
from typing import List, Tuple

import pandas as pd

from mydeep_api.dataset.column import Column
from mydeep_api.dataset.dataset import Dataset
from mydeep_api.dataset.image_path_column import ImagePathColumn
from mydeep_api.dataset.pandas_column import PandasColumn


class Data(object):
    @staticmethod
    def from_xy(x: Column, y: Column):
        return Dataset(x, y)

    @staticmethod
    def from_csv(path: str, x_col: List[str], y_col: List[str] = None) -> Dataset:
        db = pd.read_csv(path)
        return Dataset(
            x=PandasColumn(db, x_col),
            y=None if not y_col else PandasColumn(db, y_col)
        )

    @staticmethod
    def from_folder_tree(x_path: str, x_shape: Tuple[int, int] = None, y_path: str = None,
                         y_shape: Tuple[int, int] = None) -> Dataset:
        return Dataset(
            x=ImagePathColumn.from_folder_tree(x_path, x_shape),
            y=None if not y_path else ImagePathColumn.from_folder_tree(y_path, y_shape),
        )

    @staticmethod
    def from_export(path: str) -> Dataset:
        dataset_path = os.path.join(path, 'dataset.csv')
        img_path = os.path.join(path, 'img')

        db = pd.read_csv(dataset_path)
        return Dataset(
            x=ImagePathColumn(db['x'], img_path),
            y=ImagePathColumn(db['y'], img_path),
        )
