from typing import List

from editor_api.data import DataOperator
from editor_api.plugin import Plugin
from editor_plugins.tiling.operators.show_contours import ShowContours
from editor_plugins.tiling.operators.show_tiling import ShowTiling


class TilingPlugin(Plugin):
    def operators(self) -> List[type(DataOperator)]:
        return [
            ShowTiling,
            ShowContours
        ]
