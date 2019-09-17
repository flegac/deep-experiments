from typing import List

from editor.core.api.data_transformer import DataTransformer
from editor.core.api.plugin import Plugin
from plugin_0.transforms.contrast_stretching import ContrastStretchingTransform
from plugin_0.transforms.edge_detection import EdgeDetectionTransform
from plugin_0.transforms.normalize import NormalizeTransform


class Plugin0(Plugin):
    def transformers(self) -> List[type(DataTransformer)]:
        return [
            ContrastStretchingTransform,
            EdgeDetectionTransform,
            NormalizeTransform,
        ]
