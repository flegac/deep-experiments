import os

import cv2
import keras
import numpy as np

from data_toolbox.worker.worker import Worker


class ModelDisplayWorker(Worker):
    def __init__(self, model: keras.models.Model):
        self.name = model.name
        self.model = model

    def work(self, workspace: str):
        convolutions = list(filter(lambda _: isinstance(_, keras.layers.Conv2D), self.model.layers))
        first = convolutions[0]
        weights = first.get_weights()[0]
        print(self.name, weights.shape)
        self._draw_filters(workspace, weights)

    def _draw_filters(self, path: str, weights):
        w, h, feat_i, feat_o = weights.shape
        data = np.zeros((w * 8, h * 8, feat_i))
        for i in range(feat_o):
            c = int(i // 8)
            l = i % 8
            img = weights[:, :, :, i]
            data[w * c:w * c + w, h * l:h * l + h] = img

        data = 255 * (data - data.min()) / data.max()
        data = data.astype(np.uint8)
        output_path = os.path.join(path, '{}.png'.format(self.name))
        cv2.imwrite(output_path, data)
