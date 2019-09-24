import json
import os
from dataclasses import field
from pathlib import Path
from typing import List

from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass

from editor_core.editor.editor_config import EditorManager


@dataclass
class ProjectConfig:
    name: str
    workspace: str
    datasets: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=list)

    class Meta:
        fields = ("name", "workspace", "datasets", "sources")
        ordered = True
        unknown = EXCLUDE


class ProjectManager(object):
    def __init__(self):
        self.config = EditorManager.load()

    def list(self):
        return [_.parent.name for _ in self.config.root_path.glob('*/project.json')]

    def create(self, path: str):
        project = ProjectConfig(
            name=os.path.basename(path),
            workspace=path,
        )
        self.save(project)
        return project

    def load(self, name: str):
        try:
            path = self.config.root_path / name / 'project.json'
            with path.open() as _:
                return ProjectConfig.Schema().load(json.load(_))
        except:
            path = Path(name)
            with path.open() as _:
                return ProjectConfig.Schema().load(json.load(_))

    def save(self, project: ProjectConfig):
        path = self.config.root_path / project.name / 'project.json'
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open('w') as _:
            json.dump(
                ProjectConfig.Schema().dump(project),
                _, indent=4, sort_keys=True
            )


if __name__ == '__main__':
    manager = ProjectManager()
    print(manager.list())
    prj = manager.load('toto')
    print(prj)
