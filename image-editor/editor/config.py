import json
import os

from editor.api.plugin import Plugin

DEFAULT_CONFIG = {
    'dataset_selection_path': '/'
}


class EditorConfig(object):
    @staticmethod
    def from_path(path: str):
        return EditorConfig(path)

    def __init__(self, config_path: str = '/tmp/.editor/config.json'):
        self.config_path = config_path
        self.sources = []
        self.transformers = []
        self.processes = []

        self.config = DEFAULT_CONFIG
        if os.path.exists(config_path):
            with open(config_path) as _:
                self.config = json.load(_)

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as _:
            json.dump(self.config, _, indent=4, sort_keys=True)

    def load(self, plugin: Plugin):
        self.sources.extend(plugin.sources())
        self.transformers.extend(plugin.transformers())
        self.processes.extend(plugin.processes())


EDITOR = EditorConfig()
