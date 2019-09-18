from typing import List

from editor.api.data import DataTransformer
from editor.api.plugin import Plugin
from editor.plugins.tiling.transforms.tiling import TileTransformer


class TilingPlugin(Plugin):
    def transformers(self) -> List[type(DataTransformer)]:
        return [
            TileTransformer
        ]
