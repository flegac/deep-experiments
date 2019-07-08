import os
from abc import ABC
from typing import Sized, Iterable, Tuple, Iterator

import cv2
import pandas as pd
import tqdm

from mydeep_api.tensor import Tensor


class Dataset(ABC, Sized, Iterable[Tensor]):
    @property
    def shape(self) -> Tuple[int, int, int]:
        raise NotImplementedError()


class BiDataset(Sized, Iterable[Tuple[Tensor, Tensor]]):

    def __init__(self, x: Dataset, y: Dataset = None):
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
                x = _export_tensor(_x, x_path)
                y_path = os.path.join(img_path, '{}_y.png'.format(i))
                y = _export_tensor(_y, y_path) if _y is not None else None

                yield x, y

        new_df = pd.DataFrame(run(), columns=['x', 'y'])
        new_df.to_csv(os.path.join(path, 'dataset.csv'), index=False)
        return new_df


def _export_tensor(tensor: Tensor, path: str):
    if 2 <= len(tensor.shape) <= 3:
        cv2.imwrite(path, tensor)
        return os.path.basename(path)
    return tensor
