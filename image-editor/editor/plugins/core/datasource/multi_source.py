from typing import List

from editor.api.data import DataSource, Buffer
from editor.plugins.core.combiners.blend_combiner import BlendCombiner


class MultiSource(DataSource):
    def __init__(self):
        self.layers: List[DataSource] = []

    def add_layer(self, layer: DataSource):
        self.layers.append(layer)

    def __call__(self) -> Buffer:
        return BlendCombiner()([_() for _ in self.layers])
