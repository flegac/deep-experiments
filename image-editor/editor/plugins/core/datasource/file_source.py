import os

import cv2

from editor.api.data import DataSource, Buffer


class FileSource(DataSource):
    @staticmethod
    def from_gray(path: str):
        return FileSource(path, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def from_rgb(path: str):
        return FileSource(path, cv2.IMREAD_COLOR)

    def __init__(self, path: str, cv2_color_type: int):
        self.name = os.path.basename(path)
        self.path = path
        self.cv2_color_type = cv2_color_type
        self.data = None

    def __call__(self) -> Buffer:
        if self.data is None:
            self.data = cv2.imread(self.path, self.cv2_color_type)
            self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        return self.data

    def update(self):
        self.data = None
