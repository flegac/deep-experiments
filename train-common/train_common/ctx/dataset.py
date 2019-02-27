import json
import numpy as np
import pandas as pd

from surili_core.workspace import Workspace


class Dataset(object):
    @staticmethod
    def from_path(path: str):
        with open(path, 'r') as _:
            dataset = json.load(_)
        return Dataset(
            pd.read_csv(dataset['dataset_path']),
            dataset['images_path'],
            dataset['images_ext'])

    def __init__(self, dataset: pd.DataFrame, images_path: str, images_ext: str):
        self.df = dataset
        self.img_path = images_path
        self.img_ext = images_ext

    def size(self):
        return len(self.df)

    def steps_number(self, batch_size: int):
        return np.ceil(self.size() / batch_size)

    def to_path(self, path: str):
        assert path.endswith('.json'), path
        dataset_path = path.replace('.json', '.csv')
        self.df.to_csv(dataset_path, index=False)
        with open(path, 'w') as _:
            json.dump({
                'dataset_path': dataset_path,
                'images_path': self.img_path,
                'images_ext': self.img_ext
            }, _, sort_keys=True, indent=4, separators=(',', ': '))
        return path

    def __repr__(self) -> str:
        return json.dumps({
            'dataset': list(self.df),
            'img_path': self.img_path,
            'img_ext': self.img_ext
        }, sort_keys=True, separators=(',', ': '))


class TrainingDataset(object):

    @staticmethod
    def from_path(target_ws: Workspace):
        with open(target_ws.path_to('dataset.json'), 'r') as _:
            dataset = json.load(_)
        for x in dataset:
            dataset[x] = Dataset.from_path(dataset[x])
        return TrainingDataset(**dataset)

    def __init__(self, train: Dataset, test: Dataset):
        self.train = train
        self.test = test

    def to_path(self, target_ws: Workspace):
        target_path = target_ws.path_to('dataset.json')
        dataset = {
            'train': self.train.to_path(target_ws.path_to('train.json')),
            'test': self.test.to_path(target_ws.path_to('test.json')),
        }
        with open(target_path, 'w') as _:
            json.dump(dataset, fp=_, sort_keys=True, indent=4, separators=(',', ': '))
        return target_path

    def __repr__(self) -> str:
        return json.dumps({
            'train': repr(self.train),
            'test': repr(self.test)
        }, sort_keys=True, indent=4, separators=(',', ': '))
