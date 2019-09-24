import json
from dataclasses import field
from pathlib import Path

from marshmallow import EXCLUDE
from marshmallow_dataclass import dataclass

from editor_api.plugin import Plugin

EDITOR_WORKSPACE = Path.home() / '.my_editor'
EDITOR_CONFIG_PATH = EDITOR_WORKSPACE / 'config.json'


@dataclass
class EditorConfig:
    project: str = field(default=None)
    browser_path: str = field(default=str(Path.home()))
    root_path: Path = field(default=EDITOR_WORKSPACE)

    def config_path_is_valid(self, path: str):
        return not (path is None or len(path) == 0)

    class Meta:
        fields = ("project", "browser_path")
        ordered = True
        unknown = EXCLUDE


class EditorManager(object):
    plugin = Plugin()
    config: EditorConfig = None

    @staticmethod
    def load() -> EditorConfig:
        try:
            with EDITOR_CONFIG_PATH.open() as _:
                data = json.load(_)
                EditorManager.editor = EditorConfig.Schema().load(data)
        except Exception as e:
            print('an error occured :' + str(e))
            EditorManager.editor = EditorConfig()
            EditorManager.save(EditorManager.editor)
        return EditorManager.editor

    @staticmethod
    def save(config: EditorConfig):
        EDITOR_WORKSPACE.mkdir(parents=True, exist_ok=True)
        with EDITOR_CONFIG_PATH.open('w') as _:
            json.dump(EditorConfig.Schema().dump(config), _, indent=4, sort_keys=True)


if __name__ == '__main__':
    conf = EditorManager.load()
    print(conf)
    EditorManager.save(conf)
