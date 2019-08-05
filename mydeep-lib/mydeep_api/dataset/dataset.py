import os
from typing import Sized, Iterable, Tuple, Iterator

import pandas as pd
import tqdm

from mydeep_api.dataset.column import Column
from mydeep_api.tensor import Tensor
from surili_core.surili_io.image_io import OpencvIO


class Dataset(Sized, Iterable[Tuple[Tensor, Tensor]]):

    def __init__(self, x: Column, y: Column = None):
        assert y is None or len(y) == len(x)
        self.x = x
        self.y = y

    def __iter__(self) -> Iterator[Tuple[Tensor, Tensor]]:
        for _ in zip(self.x, self.y):
            yield _

    def __len__(self) -> int:
        return len(self.x)

    @property
    def is_segmentation(self):
        return self.y is None or self.x.shape == self.y.shape

    def export(self, path: str):
        path = os.path.abspath(path)
        img_path = os.path.join(path, 'img')
        os.makedirs(img_path, exist_ok=True)

        def run():
            for i, _ in tqdm.tqdm(enumerate(self), 'dataset.export({})'.format(path)):
                _x, _y = _
                x_path = os.path.join(img_path, '{}_x.png'.format(i))
                x = _export_tensor(x_path, _x)
                y_path = os.path.join(img_path, '{}_y.png'.format(i))
                y = _export_tensor(y_path, _y) if _y is not None else None

                yield x, y

        new_df = pd.DataFrame(run(), columns=['x', 'y'])
        new_df.to_csv(os.path.join(path, 'dataset.csv'), index=False)
        return new_df


def _export_tensor(path: str, tensor: Tensor):
    if 2 <= len(tensor.shape) <= 3:
        OpencvIO().write(path, tensor)
        return os.path.basename(path)
    return tensor
