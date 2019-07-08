from abc import ABC

from typing import Iterator, Sized

from mydeep_api.tensor import Tensor


class Dataset(Sized, ABC):
    @property
    def x(self) -> Iterator[Tensor]:
        raise NotImplementedError()

    @property
    def y(self) -> Iterator[Tensor]:
        raise NotImplementedError()
