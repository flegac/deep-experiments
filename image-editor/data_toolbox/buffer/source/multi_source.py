from typing import List

from data_toolbox.buffer.buffer import Buffer
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.buffer.mixer.blend_mixer import BlendMixer


class MultiSource(BufferSource):
    def __init__(self):
        self.layers: List[BufferSource] = []

    def add_layer(self, layer: BufferSource):
        self.layers.append(layer)

    def get_data(self) -> Buffer:
        return BlendMixer()(self.layers).get_buffer()

    def __repr__(self):
        return repr(self.layers)
