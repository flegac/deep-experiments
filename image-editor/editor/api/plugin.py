import abc
from typing import List

from editor.api.data import DataSource, DataTransformer
from editor.api.process import DataProcessFactory


class Plugin(abc.ABC):
    def sources(self) -> List[DataSource]:
        return []

    def transformers(self) -> List[DataTransformer]:
        return []

    def processes(self) -> List[DataProcessFactory]:
        return []
