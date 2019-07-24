import os
from typing import List, Tuple

import pandas as pd

from mydeep_api.dataset.dataset import Dataset
from mydeep_api.dataset.bi_dataset import BiDataset
from mydeep_api.dataset.file_tree_dataset import ImagePathDataset
from mydeep_api.dataset.pandas_dataset import PandasDataset


class Data(object):
    @staticmethod
    def from_xy(x: Dataset, y: Dataset):
        return BiDataset(x, y)

    @staticmethod
    def from_csv(path: str, x_col: List[str], y_col: List[str] = None) -> BiDataset:
        db = pd.read_csv(path)
        return BiDataset(
            x=PandasDataset(db, x_col),
            y=None if not y_col else PandasDataset(db, y_col)
        )

    @staticmethod
    def from_folder_tree(x_path: str, x_shape: Tuple[int, int] = None, y_path: str = None,
                         y_shape: Tuple[int, int] = None) -> BiDataset:
        return BiDataset(
            x=ImagePathDataset.from_folder_tree(x_path, x_shape),
            y=None if not y_path else ImagePathDataset.from_folder_tree(y_path, y_shape),
        )

    @staticmethod
    def from_export(path: str) -> BiDataset:
        dataset_path = os.path.join(path, 'dataset.csv')
        img_path = os.path.join(path, 'img')

        db = pd.read_csv(dataset_path)
        return BiDataset(
            x=ImagePathDataset(db['x'], img_path),
            y=ImagePathDataset(db['y'], img_path),
        )
