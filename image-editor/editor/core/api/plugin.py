import abc
from typing import List

from editor.core.api.data_process import DataProcess
from editor.core.api.data_source import DataSource
from editor.core.api.data_transformer import DataTransformer


class Plugin(abc.ABC):
    def sources(self) -> List[type(DataSource)]:
        return []

    def transformers(self) -> List[type(DataTransformer)]:
        return []

    def processes(self) -> List[type(DataProcess)]:
        return []
