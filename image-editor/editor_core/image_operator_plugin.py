from editor_api.plugin import Plugin
from editor_core.dataoperator.contrast_stretching import ContrastStretchingOperator
from editor_core.dataoperator.edge_detection import EdgeDetectionOperator
from editor_core.dataoperator.dilate import DilateOperator
from editor_core.dataoperator.erode import ErodeOperator
from editor_core.dataoperator.normalize import NormalizeOperator


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
