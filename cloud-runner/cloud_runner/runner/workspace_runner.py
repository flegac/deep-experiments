import os
import shlex
import subprocess

from cloud_runner.runner.project_runner import ProjectRunner


class WorkspaceRunner(ProjectRunner):
    def run(self):
        root_path = os.path.abspath(os.curdir)

        for name in os.listdir(root_path):
            path = os.path.abspath(os.path.join(root_path, name))
            if name.startswith('workspace') and os.path.isdir(path):
                subprocess.run(shlex.split('python runner.py'), cwd=path)
