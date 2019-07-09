from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareMnist(Worker):

    def __init__(self):
        super().__init__('Prepare raw dataset', 'raw_dataset')

    def apply(self, target_ws: Workspace):
        # TODO: prepare mnist raw dataset
        raise NotImplementedError()
