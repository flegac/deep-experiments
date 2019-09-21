import os

import cv2

from editor_api.data.data_core import DataSource, Buffer


class OpencvSource(DataSource):
    @staticmethod
    def from_gray(path: str):
        return OpencvSource(path, cv2.IMREAD_GRAYSCALE)

    @staticmethod
    def from_rgb(path: str):
        return OpencvSource(path, cv2.IMREAD_COLOR)

    def __init__(self, path: str, cv2_color_type: int):
        self.path = path
        self.cv2_color_type = cv2_color_type
        self.data = None

    def get_buffer(self) -> Buffer:
        if self.data is None:
            self.data = cv2.imread(self.path, self.cv2_color_type)
            try:
                self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
            except:
                self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)

        return self.data

    def __repr__(self):
        return os.path.basename(self.path)
