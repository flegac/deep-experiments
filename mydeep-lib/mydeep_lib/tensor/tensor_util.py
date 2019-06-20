import os
from typing import Tuple

import cv2
import numpy as np

from mydeep_lib.tensor.tensor import Tensor
from sklearn import preprocessing


def normalize(tensor: Tensor):
    if len(tensor.shape) > 2:
        raise ValueError('tensor normalizer need a vector of shape [?,?] or [?] : {}'.format(tensor.shape))
    return preprocessing.normalize(tensor)


def tensor_from_path(path: str):
    return cv2.imread(path)


def tensor_scale(factor: float):
    def apply(tensor: Tensor):
        return tensor.astype(np.float32) * factor

    return apply


def tensor_centered_window(size_x, size_y):
    def apply(tensor: Tensor):
        x = (tensor.shape[0] - size_x) // 2
        y = (tensor.shape[1] - size_y) // 2
        return tensor[x:x + size_x, y:y + size_y, :]

    return apply


def tensor_save(path: str):
    def apply(item: Tuple[str, Tensor]) -> str:
        name, tensor = item
        os.makedirs(path, exist_ok=True)
        full_filename = os.path.join(path, str(name)) + '.jpg'
        cv2.imwrite(full_filename, tensor)
        return full_filename

    return apply


def to_categorical(num_classes: int):
    def apply(y):
        """Converts a class vector (integers) to binary class matrix.

        E.g. for use with categorical_crossentropy.

        Arguments:
            y: class vector to be converted into a matrix
                (integers from 0 to num_classes).
            num_classes: total number of classes.

        Returns:
            A binary matrix representation of the input. The classes axis is placed
            last.
        """
        y = np.array(y, dtype='int')
        input_shape = y.shape
        if input_shape and input_shape[-1] == 1 and len(input_shape) > 1:
            input_shape = tuple(input_shape[:-1])
        y = y.ravel()
        n = y.shape[0]
        categorical = np.zeros((n, num_classes), dtype=np.float32)
        categorical[np.arange(n), y] = 1
        output_shape = input_shape + (num_classes,)
        categorical = np.reshape(categorical, output_shape)
        return categorical

    return apply
