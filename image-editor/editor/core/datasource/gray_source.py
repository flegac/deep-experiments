import os

import cv2

from editor.core.api.data_source import DataSource


class GraySource(DataSource):
    def __init__(self, path: str):
        self.name = os.path.basename(path)
        self.data = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    def get_buffer(self):
        return self.data
