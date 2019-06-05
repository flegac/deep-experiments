import filecmp
import shutil

from surili_core.workspace import Workspace
import inspect
import os


class PipelineContext(object):
    def __init__(self, root_path: str, project_name: str):
        self.seed = 5435342
        self.root_ws = Workspace.from_path(root_path)
        self.project_ws = self.root_ws.get_ws(os.path.join('_Projects', 'alpha', project_name))
        self.max_batch_size = 256

        running_script_path = get_running_script_path()
        script_destination_path = self.project_ws.path_to('script.py.txt')
        if not os.path.exists(script_destination_path):
            shutil.copyfile(running_script_path, script_destination_path)
        elif not filecmp.cmp(running_script_path, script_destination_path, shallow=False):
            raise ValueError('Existing project {}: but running script has changed !'.format(self.project_ws.path))


def get_running_script_path():
    return os.path.abspath(inspect.stack()[-1][1])
