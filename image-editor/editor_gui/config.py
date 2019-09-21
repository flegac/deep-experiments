import json
import os
from pathlib import Path

from editor_api.plugin import Plugin

DEFAULT_CONFIG = {
    'default_project': None,
    'file_browser_path': '/',
    'project_browser_path': '/'
}
DEFAULT_ROOT_PATH = Path.home() / '.my_editor'

DEFAULT_CONFIG_PATH = DEFAULT_ROOT_PATH / 'config.json'


class EditorConfig(Plugin):
    @staticmethod
    def from_path(path: str):
        return EditorConfig(path)

    def __init__(self, config_path: str = None):
        super().__init__()
        self.config_path = config_path or str(DEFAULT_CONFIG_PATH)
        self.config = DEFAULT_CONFIG
        if os.path.exists(self.config_path):
            with open(self.config_path) as _:
                self.config = json.load(_)

    def config_path_is_valid(self, param: str):
        path = self.config.get(param)
        return not (path is None or len(path) == 0)

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as _:
            json.dump(self.config, _, indent=4, sort_keys=True)


EDITOR_CONFIG = EditorConfig()
