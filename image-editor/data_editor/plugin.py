import abc
from typing import List

from data_toolbox.data.data_operator import DataOperator
from data_toolbox.buffer.operator.contrast_stretching import ContrastStretchingOperator
from data_toolbox.buffer.operator.dilate import DilateOperator
from data_toolbox.buffer.operator.edge_detection import EdgeDetectionOperator
from data_toolbox.buffer.operator.erode import ErodeOperator
from data_toolbox.buffer.operator.normalize import NormalizeOperator
from data_toolbox.buffer.operator.show_contours import ShowContours
from data_toolbox.buffer.operator.show_tiling import ShowTiling


class Plugin(abc.ABC):
    def __init__(self):
        self._operators: List[type(DataOperator)] = []

    def operators(self) -> List[type(DataOperator)]:
        return self._operators

    def extend(self, plugin: 'Plugin'):
        self._operators.extend(plugin.operators())


class ImageFilterPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.operators().extend([
            NormalizeOperator,
            ContrastStretchingOperator,
            EdgeDetectionOperator,
            DilateOperator,
            ErodeOperator
        ])


class VisuPlugin(Plugin):
    def __init__(self):
        super().__init__()
        self.operators().extend([
            ShowTiling,
            ShowContours
        ])
