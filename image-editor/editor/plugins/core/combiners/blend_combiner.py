from typing import List

import cv2
import numpy as np

from editor.api.data import DataCombiner, Buffer


class BlendCombiner(DataCombiner):
    def __call__(self, buffers: List[Buffer]) -> Buffer:
        if len(buffers) == 0:
            return np.zeros((10, 10, 3)).astype('uint8')

        result = buffers[0].astype('float64')

        for buffer in buffers[1:]:
            print(result.shape, buffer.shape)
            if result.shape != buffer.shape:
                buffer = cv2.resize(buffer, result.shape[:2][::-1])
            print(result.shape, buffer.shape)

            result = cv2.add(result, buffer.astype('float64'))
        result = result / len(buffers)
        return result.astype('uint8')
