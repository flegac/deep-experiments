import json
import os
from pathlib import Path

from editor_api.plugin import Plugin
from editor_plugins.image_filter.plugin import ImageFilterPlugin
from editor_plugins.morphology.plugin import MorphologyPlugin
from editor_plugins.tiling.plugin import TilingPlugin

DEFAULT_CONFIG = {
    'file_browser_path': '/',
    'project_browser_path': '/'
}
DEFAULT_CONFIG_PATH = str(Path.home() / '.my_editor/config.json')


class EditorConfig(Plugin):
    @staticmethod
    def from_path(path: str):
        return EditorConfig(path)

    def __init__(self, config_path: str = DEFAULT_CONFIG_PATH):
        super().__init__()
        self.config_path = config_path

        self.config = DEFAULT_CONFIG
        if os.path.exists(config_path):
            with open(config_path) as _:
                self.config = json.load(_)

    def config_path_is_valid(self, param: str):
        path = self.config.get(param)
        return not (path is None or len(path) == 0)

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as _:
            json.dump(self.config, _, indent=4, sort_keys=True)


EDITOR_CONFIG = EditorConfig()
EDITOR_CONFIG.extend(ImageFilterPlugin())
EDITOR_CONFIG.extend(MorphologyPlugin())
EDITOR_CONFIG.extend(TilingPlugin())
