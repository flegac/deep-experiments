import os
from typing import List

import cv2
import numpy as np

from editor.core.api.data_pipeline import DataProvider
from editor.core.provider.band import Band


class MultiBand(DataProvider):

    def __init__(self, name: str):
        self.name = name
        self.bands: List[Band] = []

    def open(self, path: str):
        name = os.path.basename(path)
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        if len(img.shape) == 3:
            for i in range(img.shape[2]):
                self.bands.append(Band('{}_{}'.format(name, i), img, i))

    def get_buffer(self):
        # return np.dstack([_.get_buffer() for _ in random.choices(population=self.bands, k=3)])
        return np.dstack([_.get_buffer() for _ in self.bands])
