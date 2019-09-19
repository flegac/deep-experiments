from typing import List

from editor.core.data import DataTransformer, DataSource
from editor.core.plugin import Plugin
from editor.core.process import DataProcess
from editor.plugins.core.datasource.buffer_source import BufferSource
from editor.plugins.core.datasource.cached_source import CachedSource
from editor.plugins.core.datasource.file_source import FileSource
from editor.plugins.core.datasource.multi_source import MultiSource
from editor.plugins.core.transforms.pipeline import Pipeline
from editor.plugins.core.transforms.viewport import ViewportTransformer


class CorePlugin(Plugin):
    def sources(self) -> List[type(DataSource)]:
        return [
            BufferSource,
            FileSource,
            MultiSource,
            CachedSource
        ]

    def transformers(self) -> List[type(DataTransformer)]:
        return [
            Pipeline,
            ViewportTransformer
        ]

    def processes(self) -> List[DataProcess]:
        return [

        ]
