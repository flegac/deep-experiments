from editor.core.api.plugin import Plugin


class PluginManager(object):
    def __init__(self):
        self.sources = set()
        self.transformers = set()
        self.processes = set()

    def load(self, plugin: Plugin):
        self.sources.update(plugin.sources())
        self.transformers.update(plugin.transformers())
        self.processes.update(plugin.processes())


PLUGIN_MANAGER = PluginManager()
