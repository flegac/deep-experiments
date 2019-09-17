from typing import List

from editor.core.api.data_transformer import DataTransformer
from editor.core.api.plugin import Plugin
from editor_plugin.img_transform.contrast_stretching import ContrastStretchingTransform
from editor_plugin.img_transform.edge_detection import EdgeDetectionTransform
from editor_plugin.img_transform.normalize import NormalizeTransform


class Plugin0(Plugin):

    def transformers(self) -> List[DataTransformer]:
        return [
            ContrastStretchingTransform(),
            EdgeDetectionTransform(),
            NormalizeTransform(),
        ]
