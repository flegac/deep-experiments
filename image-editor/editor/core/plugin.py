import abc
from typing import List

from editor.core.data import DataSource, DataTransformer
from editor.core.process import DataProcessFactory


class Plugin(abc.ABC):
    def sources(self) -> List[DataSource]:
        return []

    def transformers(self) -> List[DataTransformer]:
        return []

    def processes(self) -> List[DataProcessFactory]:
        return []
