from typing import List

from editor_api.data.data_operator import DataOperator
from editor_api.plugin import Plugin
from editor_core.stats_visus.show_contours import ShowContours
from editor_core.stats_visus.show_tiling import ShowTiling


class VisuPlugin(Plugin):
    def operators(self) -> List[type(DataOperator)]:
        return [
            ShowTiling,
            ShowContours
        ]
