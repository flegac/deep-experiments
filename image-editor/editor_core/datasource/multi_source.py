from typing import List

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataSource
from editor_core.dataoperator.blend_mixer import BlendMixer


class MultiSource(DataSource):
    def __init__(self):
        self.layers: List[DataSource] = []

    def add_layer(self, layer: DataSource):
        self.layers.append(layer)

    def get_buffer(self) -> Buffer:
        return BlendMixer()(self.layers).get_buffer()

    def __repr__(self):
        return repr(self.layers)
