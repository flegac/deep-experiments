from typing import List

import cv2
import numpy as np

from editor_api.data import DataMixer, Buffer


class BlendMixer(DataMixer):
    def apply(self, buffers: List[Buffer]) -> Buffer:
        if len(buffers) == 0:
            return np.zeros((10, 10, 3)).astype('uint8')

        result = buffers[0].astype('float64')

        for buffer in buffers[1:]:
            if result.shape != buffer.shape:
                buffer = cv2.resize(buffer, result.shape[:2][::-1])
            result = cv2.add(result, buffer.astype('float64'))
        result = result / len(buffers)
        return result.astype('uint8')
