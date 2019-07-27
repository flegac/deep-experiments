import os

from surili_core.workspace import Workspace


class PipelineContext(object):
    def __init__(self, project_name: str, root_path: str):
        self.seed = 5435342
        self.project_name = project_name
        self.workspace = Workspace.from_path(os.path.join(root_path, project_name))
        self.max_batch_size = 256
