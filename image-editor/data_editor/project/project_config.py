import json
import os
from dataclasses import field
from pathlib import Path

from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass

from data_editor.editor.editor_config import EditorManager


@dataclass
class ProjectConfig:
    name: str
    workspace: str
    image_path: str = field(default='images')
    table_path: str = field(default='tables')
    model_path: str = field(default='models')

    class Meta:
        fields = ('name', 'workspace', 'image_path')
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
        except Exception as e:
            print(e)
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
    prj = manager.load('my_project1')
    print(prj)
