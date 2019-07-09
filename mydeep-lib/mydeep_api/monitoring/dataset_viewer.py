import math
from itertools import islice

import numpy as np
from matplotlib import pyplot as plt

from mydeep_api.dataset.dataset import Dataset


class DatasetViewer(object):
    def __init__(self,
                 dataset: Dataset,
                 label: str,
                 scale: float,
                 ):
        self.dataset = dataset
        self.label = label
        self.scale = scale

    def show(self, n: int = None):
        self._plot(n).show()

    def save(self, path: str, n: int = None):
        self._plot(n).savefig(path)

    def _plot(self, n: int):
        self.number = min(n, len(self.dataset)) if n is not None else len(self.dataset)

        label = "{}: {} samples".format(self.label, self.number)

        cols = 5
        lines = math.ceil(self.number / cols)

        fig, ax = plt.subplots(nrows=lines, ncols=cols, figsize=(self.scale * cols, self.scale * lines))
        ax = ax.reshape(cols * lines)
        ax[0].set_title(label, size='large')

        for i, x in enumerate(islice(self.dataset, self.number)):
            if x.shape[2] != 3:
                x = np.moveaxis(x, 0, 2)
            x = (x * 255 / np.max(x)).astype(np.uint8)
            ax[i].imshow(x)
        for i in range(len(ax)):
            ax[i].axis('off')
        return plt
