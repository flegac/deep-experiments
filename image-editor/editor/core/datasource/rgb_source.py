import os

import cv2

from editor.core.api.data_source import DataSource


class RGBSource(DataSource):

    def __init__(self, path: str):
        self.name = os.path.basename(path)
        img = cv2.imread(path, cv2.IMREAD_COLOR)
        self.data = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def get_buffer(self):
        return self.data
