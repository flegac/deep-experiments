import math

import numpy as np
from matplotlib import pyplot as plt

from stream_lib.stream import stream
from stream_lib.stream_api import Stream


class ShowDataset(object):
    def __init__(self, label: str, scale: float):
        self.label = label
        self.scale = scale

    def apply(self, samples: Stream):
        data = samples.to_list()
        n = len(data)
        if n == 0:
            return stream(data)

        label = "{}: {} samples".format(self.label, n)

        cols = 5
        lines = math.ceil(n / cols)

        fig, ax = plt.subplots(nrows=lines, ncols=cols, figsize=(self.scale * cols, self.scale * lines))
        ax = ax.reshape(cols * lines)
        ax[0].set_title(label, size='large')

        for i, sample in enumerate(data):
            x = sample.x
            if x.shape[2] != 3:
                x = np.moveaxis(x, 0, 2)
            ax[i].imshow(x)
        for i in range(len(data), len(ax)):
            ax[i].axis('off')
        fig.show()

        return stream(data)
