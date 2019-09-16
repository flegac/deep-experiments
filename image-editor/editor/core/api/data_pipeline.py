import abc

import numpy as np


class DataProvider(abc.ABC):
    def get_buffer(self) -> np.ndarray:
        raise NotImplementedError()

    def with_transform(self, transform: 'DataTransform') -> 'DataProvider':
        return _TransformedProvider(self, transform)


class DataTransform(abc.ABC):
    def apply(self, data: np.ndarray) -> np.ndarray:
        raise NotImplementedError()

    def with_provider(self, provider: DataProvider) -> DataProvider:
        return _TransformedProvider(provider, self)


class _TransformedProvider(DataProvider):
    def __init__(self, provider: DataProvider, transform: DataTransform):
        self.provider = provider
        self.transform = transform

    def get_buffer(self) -> np.ndarray:
        return self.transform.apply(self.provider.get_buffer())
