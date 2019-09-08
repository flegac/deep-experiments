import numpy as np
from skimage import exposure

from mydeep_api.tensor import Tensor


def contrast_stretching(img: Tensor) -> Tensor:
    p2, p98 = np.percentile(img, (2, 98))
    return exposure.rescale_intensity(img, in_range=(p2, p98))


def adaptive_equalization(img: Tensor) -> Tensor:
    return exposure.equalize_adapthist(img, clip_limit=0.03) * 255


def hist_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))
    return intersection

