import pandas as pd

from mydeep_api._deprecated.file_dataset import FileDataset
from surili_core.workspace import Workspace
from mydeep_api._deprecated.train_dataset import TrainDataset

ws = Workspace.from_path('./resources/generated/dataset')


def test_dataset_to_path():
    train = FileDataset(
        pd.DataFrame({'a': [1, 2], 'b': [3, 4]}),
        '/path/to/images',
        'jpg')
    dataset = TrainDataset(train, train)
    dataset.to_path(ws)


def test_dataset_from_path():
    dataset = TrainDataset.from_path(ws)
    print(dataset)


