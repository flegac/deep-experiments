import os
from typing import Tuple

import cv2

from editor_api.data import DataSource, Buffer


class OpencvSource(DataSource):
    def __init__(self, path: str, cv2_color_type: int):
        self.path = path
        self.cv2_color_type = cv2_color_type
        self.data = None

    def get_buffer(self, offset: Tuple[int, int], size: Tuple[int, int]) -> Buffer:
        if self.data is None:
            self.data = cv2.imread(self.path, self.cv2_color_type)
            try:
                self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
            except:
                self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2GRAY)

        return self.data if offset is None else self.data[offset[1]:offset[0], size[1]: size[0]]

    def __repr__(self):
        return os.path.basename(self.path)
