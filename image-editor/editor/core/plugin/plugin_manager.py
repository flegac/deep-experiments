import json
import os

from editor.core.api.plugin import Plugin

DEFAULT_CONFIG = {
    'dataset_selection_path': '/'
}


class Editor(object):
    def __init__(self, config_path: str = '/tmp/.editor/config.json'):
        self.config_path = config_path
        self.sources = set()
        self.transformers = set()
        self.processes = set()

        self.config = DEFAULT_CONFIG
        if os.path.exists(config_path):
            with open(config_path) as _:
                self.config = json.load(_)

    def save_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as _:
            json.dump(self.config, _, indent=4, sort_keys=True)

    def load(self, plugin: Plugin):
        self.sources.update(plugin.sources())
        self.transformers.update(plugin.transformers())
        self.processes.update(plugin.processes())


EDITOR = Editor()
