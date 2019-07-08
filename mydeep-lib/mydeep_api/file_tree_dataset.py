import os

import cv2
from typing import Iterator

from mydeep_api.dataset import Dataset
from mydeep_api.tensor import Tensor


class FileTreeDataset(Dataset):
    def __init__(self, x_path: str, y_path: str):
        self.x_path = x_path
        self.y_path = y_path

    @property
    def x(self) -> Iterator[Tensor]:
        for cat in os.listdir(self.x_path):
            for file in os.listdir(os.path.join(self.x_path, cat)):
                yield cv2.imread(os.path.join(self.x_path, cat, file))

    @property
    def y(self) -> Iterator[Tensor]:
        for cat in os.listdir(self.y_path):
            for file in os.listdir(os.path.join(self.y_path, cat)):
                yield cv2.imread(os.path.join(self.y_path, cat, file))

    def __len__(self):
        raise NotImplementedError()
