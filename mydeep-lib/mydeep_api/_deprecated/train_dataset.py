import json

from mydeep_api._deprecated.file_dataset import FileDataset
from surili_core.workspace import Workspace


class TrainDataset(object):

    @staticmethod
    def from_path(target_ws: Workspace):
        with open(target_ws.path_to('dataset.json'), 'r') as _:
            dataset = json.load(_)
        for x in dataset:
            dataset[x] = FileDataset.from_path(dataset[x])
        return TrainDataset(**dataset)

    def __init__(self, train: FileDataset, test: FileDataset):
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
