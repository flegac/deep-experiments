import json

from surili_core.pipelines import pipeline, step
from surili_core.surili_io.storage_io import StorageExport
from surili_core.workspace import Workspace

with open('config.json') as _:
    config = json.load(_)

if __name__ == "__main__":
    _ = Workspace.from_path('/tmp/.workspace/my_workspace')
    pipeline(
        steps=[
            step(step_id='step_01', worker=StorageExport('gs://flegac-test/cloud_runner')),
        ]
    )(_)
