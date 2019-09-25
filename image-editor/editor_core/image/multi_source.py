from typing import List

from editor_api.data.buffer import Buffer
from editor_api.data.data_source import ImageSource
from editor_core.dataoperator.blend_mixer import BlendMixer


class MultiSource(ImageSource):
    def __init__(self):
        self.layers: List[ImageSource] = []

    def add_layer(self, layer: ImageSource):
        self.layers.append(layer)

    def get_data(self) -> Buffer:
        return BlendMixer()(self.layers).get_buffer()

    def __repr__(self):
        return repr(self.layers)
