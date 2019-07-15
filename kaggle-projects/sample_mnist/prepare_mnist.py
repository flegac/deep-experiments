from surili_core.worker import Worker
from surili_core.workspace import Workspace


class PrepareMnist(Worker):

    def run(self, ctx, target_ws: Workspace):
        # TODO: prepare mnist raw dataset
        raise NotImplementedError()
