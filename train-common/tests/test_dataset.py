import pandas as pd

from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset, TrainingDataset

ws = Workspace.from_path('./resources/dataset')


def test_dataset_to_path():
    train = Dataset(
        pd.DataFrame({'a': [1, 2], 'b': [3, 4]}),
        '/path/to/images',
        'jpg')
    dataset = TrainingDataset(train, train)
    dataset.to_path(ws.path_to('dataset.json'))


def test_dataset_from_path():
    dataset = TrainingDataset.from_path(ws)
    print(dataset)


test_dataset_to_path()

test_dataset_from_path()
