import os
from typing import Iterator, Tuple, List

import cv2

from mydeep_api.dataset.column import Column
from mydeep_api.tensor import Tensor
from surili_core.workspace import Workspace


class ImagePathColumn(Column):
    @staticmethod
    def from_folder_tree(path: str, shape: Tuple[int, int] = None):
        images = (Workspace.from_path(path)
                  .folders
                  .flatmap(lambda fs: fs.files)
                  .map(lambda p: os.path.relpath(p, start=path))
                  .to_list())
        return ImagePathColumn(images, path, shape)

    def __init__(self, images: List[str],
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
