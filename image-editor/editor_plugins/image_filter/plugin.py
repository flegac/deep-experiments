from editor_api.plugin import Plugin
from editor_plugins.image_filter.operators.contrast_stretching import ContrastStretchingOperator
from editor_plugins.image_filter.operators.edge_detection import EdgeDetectionOperator
from editor_plugins.image_filter.operators.normalize import NormalizeOperator


class ImageFilterPlugin(Plugin):
    def __init__(self):
        super().__init__()

        self.operators().extend([
            NormalizeOperator,
            ContrastStretchingOperator,
            EdgeDetectionOperator,
        ])
