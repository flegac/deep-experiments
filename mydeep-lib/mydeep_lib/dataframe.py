import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from surili_core.workspace import Workspace


class Dataframes:
    @staticmethod
    def from_csv(path: str):
        return pd.read_csv(path)

    @staticmethod
    def to_csv(path: str):
        def apply(dataframe: pd.DataFrame) -> str:
            dataframe.to_csv(path, index=False)
            return path

        return apply

    @staticmethod
    def from_directory_structure(x_key: str = 'x', y_key: str = 'y'):
        def apply(path: str):
            data = Workspace.from_path(path) \
                .files() \
                .map(Workspace.from_path) \
                .flatmap(lambda fs: fs.files()) \
                .map(lambda f: (f, os.path.basename(os.path.dirname(f)))) \
                .to_list()
            data = np.array(data)
            data = pd.DataFrame(data, columns=[x_key, y_key])
            return data

        return apply

    @staticmethod
    def split_by_key(key: str):
        def apply(dataframe: pd.DataFrame) -> dict:
            result = {}
            for x in set(dataframe[key].values):
                result[x] = dataframe[dataframe[key] == x]
            return result

        return apply

    @staticmethod
    def split(test_size: float, key: str = None):
        def apply(dataframe: pd.DataFrame):
            if key:
                return train_test_split(dataframe, test_size=test_size, stratify=dataframe[key])
            return train_test_split(dataframe, test_size=test_size)

        return apply

    @staticmethod
    def train_test_split(test_size: float, key: str = None):
        return Dataframes.split(test_size, key)
