from typing import List, Tuple

from editor_api.data.data_core import DataSource, Buffer
from editor_core.blend_mixer import BlendMixer


class MultiSource(DataSource):
    def __init__(self):
        self.layers: List[DataSource] = []

    def add_layer(self, layer: DataSource):
        self.layers.append(layer)

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        return BlendMixer()([_.get_buffer(offset, size) for _ in self.layers])

    def __repr__(self):
        return repr(self.layers)
