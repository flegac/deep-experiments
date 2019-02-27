import cv2
import random

import numpy as np

from mydeep_lib.tensor.tensor import Tensor


def augment_light(brightness: float, contrast: float):
    def apply(tensor: Tensor):
        tensor = tensor + brightness
        tensor = tensor * contrast
        tensor = np.clip(tensor, 0, 1.0)
        return tensor

    return apply


def flip(flip_x: bool, flip_y: bool):
    def apply(tensor: Tensor):
        if flip_y:
            tensor = tensor[:, ::-1]
        if flip_x:
            tensor = tensor[::-1, :]
        return tensor

    return apply


def rotate(rotation: float):
    def apply(tensor: Tensor):
        original_size = tensor.shape
        M = cv2.getRotationMatrix2D((original_size[0] / 2, original_size[1] / 2), rotation, 1)
        tensor = cv2.warpAffine(tensor, M, (original_size[0], original_size[1]))
        return tensor

    return apply


def shift(dx: int, dy: int):
    def apply(tensor: Tensor):
        tensor = tensor[:, dx:, :] if dx >= 0 else tensor[:, :dx, :]
        tensor = tensor[dy:, :, :] if dy >= 0 else tensor[:dy, :, :]
        return tensor

    return apply


def tensor_augment(crop_size=(0, 0), rotation=0, shift=0, brightness=0, contrast=0):
    def apply(tensor: np.ndarray):
        # random rotation
        rot = random.randint(-rotation, rotation)
        tensor = rotate(rot)(tensor)

        # random x,y-shift
        x = random.randint(-shift, shift)
        y = random.randint(-shift, shift)

        # crop to center
        original_size = tensor.shape
        start_crop_x = (original_size[0] - crop_size[0]) // 2
        end_crop_x = start_crop_x + crop_size[0]
        start_crop_y = (original_size[1] - crop_size[1]) // 2
        end_crop_y = start_crop_y + crop_size[1]
        tensor = tensor[(start_crop_x + x):(end_crop_x + x), (start_crop_y + y):(end_crop_y + y)]

        # Random flip
        flip_y = bool(random.getrandbits(1))
        flip_x = bool(random.getrandbits(1))
        tensor = flip(flip_x, flip_y)(tensor)

        # Random light
        br = random.randint(-brightness, brightness) / 100.
        cr = 1.0 + random.randint(-contrast, contrast) / 100.
        tensor = augment_light(brightness=br, contrast=cr)(tensor)

        return tensor

    return apply
