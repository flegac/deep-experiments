import abc

import numpy as np

from editor.core.api.data_source import DataSource


class DataTransformer(abc.ABC):
    def apply(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def with_provider(self, provider: DataSource) -> DataSource:
        return _TransformedProvider(provider, self)


class _TransformedProvider(DataSource):
    def __init__(self, provider: DataSource, transform: DataTransformer):
        self.provider = provider
        self.transform = transform

    def get_buffer(self) -> np.ndarray:
        return self.transform.apply(self.provider.get_buffer())
