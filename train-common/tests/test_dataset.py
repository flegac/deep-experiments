import pandas as pd

from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset
from train_common.ctx.train_dataset import TrainDataset

ws = Workspace.from_path('./resources/dataset')


def test_dataset_to_path():
    train = Dataset(
        pd.DataFrame({'a': [1, 2], 'b': [3, 4]}),
        '/path/to/images',
        'jpg')
    dataset = TrainDataset(train, train)
    dataset.to_path(ws.path_to('dataset.json'))


def test_dataset_from_path():
    dataset = TrainDataset.from_path(ws)
    print(dataset)


test_dataset_to_path()

test_dataset_from_path()
