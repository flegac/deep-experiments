from typing import List

from editor.core.data import DataTransformer
from editor.core.plugin import Plugin
from editor.plugins.tiling.transforms.tiling import TileTransformer


class TilingPlugin(Plugin):
    def transformers(self) -> List[type(DataTransformer)]:
        return [
            TileTransformer
        ]
