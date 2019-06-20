import os
import random

import sklearn
from scipy.ndimage import gaussian_filter
from skimage.measure import block_reduce
from tqdm import tqdm

from mydeep_lib.tensor.tensor import Tensor
from mydeep_lib.tensor.tensor_util import tensor_from_path, tensor_save
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace

import numpy as np

from skimage import filters
import matplotlib.pyplot as plt


def extract_features(rgb: Tensor):
    gray = np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    # gray = gaussian_filter(gray, sigma=1)
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    gray = (gray - np.mean(gray)) / np.std(gray)
    gray = sklearn.preprocessing.normalize(gray)
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    gray = block_reduce(gray, block_size=(2, 2), func=np.mean)
    # plt.imshow(gray, cmap='gray', interpolation='nearest').figure.show()

    val = filters.threshold_otsu(gray)
    mask = gray < val
    # plt.imshow(mask, cmap='gray', interpolation='nearest').figure.show()
    mask = mask.astype('uint8')
    mask *= 255
    mask = np.stack([mask, mask, mask])
    mask = np.moveaxis(mask, 0, 2)
    return mask


class TresholdFilter(PipelineWorker):

    def __init__(self):
        super().__init__('Treshold filter', 'treshold_filter')
        self.col_x = 'x'
        self.col_y = 'y'

    def apply(self, target_ws: Workspace):
        self.ctx.project_ws \
            .get_ws('raw_dataset/images') \
            .files() \
            .map(tensor_from_path) \
            .map(extract_features) \
            .enumerate() \
            .foreach(tensor_save(target_ws.path_to('images')))
