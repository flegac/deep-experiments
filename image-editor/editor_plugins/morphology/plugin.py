from editor_api.plugin import Plugin
from editor_plugins.morphology.operators.dilate import DilateOperator
from editor_plugins.morphology.operators.erode import ErodeOperator


class MorphologyPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.operators().extend([
            DilateOperator,
            ErodeOperator
        ])
