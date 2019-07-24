from abc import ABC
from typing import Sized, Iterable, Tuple

from mydeep_api.tensor import Tensor


class Dataset(ABC, Sized, Iterable[Tensor]):
    @property
    def shape(self) -> Tuple[int, int, int]:
        raise NotImplementedError()


