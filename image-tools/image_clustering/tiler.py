from typing import Tuple, Generator, Any

from mydeep_api.tensor import Tensor


class Box(object):
    @staticmethod
    def from_limits(top: int, bottom: int, left: int, right: int):
        return Box(top, left, bottom - top, right - left)

    def __init__(self, top: int, left: int, v_size: int, h_size: int):
        self.top = top
        self.left = left
        self.bottom = top + v_size
        self.right = left + h_size

    @property
    def h_size(self):
        return self.right - self.left

    @property
    def v_size(self):
        return self.bottom - self.top

    def cut(self, img: Tensor):
        result = img[self.top:self.bottom, self.left:self.right]
        if result is None:
            raise ValueError('')
        return result

    def __repr__(self) -> str:
        return 'Box[{},{}]({},{})'.format(self.v_size, self.h_size, self.top, self.left)


class Tiler(object):
    def __init__(self, tile_number: Tuple[int, int]):
        self.tile_number = tile_number

    def tiles(self, source_shape: Tuple[int, int]) -> Generator[Box, Any, None]:
        split0 = start_indexes(source_shape[0], self.tile_number[0])
        sizes0 = chunk_sizes(source_shape[0], self.tile_number[0])
        split1 = start_indexes(source_shape[1], self.tile_number[1])
        sizes1 = chunk_sizes(source_shape[1], self.tile_number[1])
        for i in range(len(split0)):
            for j in range(len(split1)):
                yield Box(split1[j], split0[i], sizes1[j], sizes0[i])


class GridTiler(object):

    def __init__(self, tile_size: int, stride: int = None):
        self.tile_size = tile_size
        self.stride = stride or tile_size

    def tiles(self, source_shape: Tuple[int, int]) -> Generator[Box, Any, None]:
        for top in range(0, source_shape[0] - self.tile_size, self.stride):
            for left in range(0, source_shape[1] - self.tile_size, self.stride):
                yield Box(top, left, self.tile_size, self.tile_size)


def chunk_sizes(n: int, k: int):
    return [(n // k) + (1 if i < (n % k) else 0) for i in range(k)]


def start_indexes(n: int, k: int):
    return [i * (n // k) + min(i, n % k) for i in range(k)]
