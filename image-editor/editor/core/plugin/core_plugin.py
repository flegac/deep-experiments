from typing import List

from editor.core.api.data_process import DataProcess
from editor.core.api.data_source import DataSource
from editor.core.api.data_transformer import DataTransformer
from editor.core.api.plugin import Plugin
from editor.core.datasource.gray_source import GraySource
from editor.core.datasource.rgb_source import RGBSource


class CorePlugin(Plugin):
    def sources(self) -> List[type(DataSource)]:
        return [
            RGBSource,
            GraySource
        ]

    def transformers(self) -> List[DataTransformer]:
        return [

        ]

    def processes(self) -> List[DataProcess]:
        return [

        ]
