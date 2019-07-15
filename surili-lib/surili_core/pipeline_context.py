import os

from surili_core.workspace import Workspace


# TODO: simplify / remove this class
# each project should redefine its own contextual state
class PipelineContext(object):
    def __init__(self, root_path: str, project_name: str):
        self.seed = 5435342
        self.root_ws = Workspace.from_path(root_path)
        self.project_ws = self.root_ws.get_ws(os.path.join('_Projects', 'alpha', project_name))
        self.max_batch_size = 256
