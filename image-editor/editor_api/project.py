import json
import os
from pathlib import Path
from typing import List


class Project(object):
    @staticmethod
    def from_path(path: str):
        try:
            project_config = str(Path(path) / '.project.json')
            with open(project_config) as _:
                config = json.load(_)
            return Project(
                name=config['name'],
                workspace=config['workspace'],
                datasets=config['datasets'],
                sources=config['sources']
            )
        except:
            project = Project(
                name=os.path.basename(path),
                workspace=path,
                datasets=[],
                sources=[]
            )
            return project

    def __init__(self, name: str, workspace: str, datasets: List[str], sources: List[str]):
        self.name = name
        self.workspace = workspace
        self.datasets = datasets
        self.sources = sources

    def save(self):
        with open(str(Path(self.workspace) / '.project.json'.format(self.name)), 'w') as _:
            json.dump({
                'name': self.name,
                'workspace': self.workspace,
                'datasets': self.datasets,
                'sources': self.sources,

            }, _, indent=4, sort_keys=True)
