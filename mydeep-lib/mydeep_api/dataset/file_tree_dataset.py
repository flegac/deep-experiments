import os
from typing import Iterator, Tuple, Collection

import cv2

from mydeep_api.dataset.dataset import Dataset
from mydeep_api.tensor import Tensor


class ImagePathDataset(Dataset):
    @staticmethod
    def from_folder_tree(path: str, shape: Tuple[int, int] = None):
        categories = [_ for _ in os.listdir(path)]
        images = [
            os.path.join(cat, file)
            for cat in categories
            for file in os.listdir(os.path.join(path, cat))
        ]
        return ImagePathDataset(images, path, shape)

    def __init__(self, images: Collection[str],
                 root_path: str = None,
                 shape: Tuple[int, int] = None):
        self.images = images
        self.root_path = root_path
        self._shape = shape

    def __iter__(self) -> Iterator[Tensor]:
        for filename in self.images:
            if self.root_path:
                filename = os.path.join(self.root_path, filename)
            yield (cv2.imread(filename))

    def __len__(self):
        return len(self.images)

    @property
    def shape(self) -> Tuple[int, int, int]:
        if self._shape:
            return next(iter(self)).shape
        return None
