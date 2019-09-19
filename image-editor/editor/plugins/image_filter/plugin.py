from typing import List

from editor.core.data import DataTransformer
from editor.core.plugin import Plugin
from editor.plugins.image_filter.transforms.core import DilateTransformer, ErodeTransformer
from editor.plugins.image_filter.transforms.edge_detection import EdgeDetectionTransform, FindContours
from editor.plugins.image_filter.transforms.normalize import NormalizeTransform, ContrastStretchingTransform


class ImageFilterPlugin(Plugin):
    def transformers(self) -> List[type(DataTransformer)]:
        return [
            NormalizeTransform,
            ContrastStretchingTransform,
            EdgeDetectionTransform,
            FindContours,
            DilateTransformer,
            ErodeTransformer
        ]
