from typing import List

import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage import exposure, transform

from mydeep_api.tensor import Tensor



def adaptive_equalization(img: Tensor) -> Tensor:
    return exposure.equalize_adapthist(img, clip_limit=0.03) * 255


def eq_hsv(img):
    band = 1
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, band] = cv2.equalizeHist(hsv[:, :, band])
    hist_equalization_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return hist_equalization_result


def eq_hist(img):
    for i in range(3):
        img[:, :, i] = cv2.equalizeHist(img[:, :, i])
    return img


def hist_intersection(hist_1, hist_2):
    minima = np.minimum(hist_1, hist_2)
    intersection = np.true_divide(np.sum(minima), np.sum(hist_2))
    return intersection


def match_hist(img: Tensor, reference: Tensor):
    return transform.match_histograms(img, reference=reference, multichannel=True)


def compute_std(paths: List[str]):
    averages = []
    stds = []
    for _ in paths:
        img = cv2.imread(_)
        averages.append(np.average(img, axis=(0, 1)))
        stds.append(np.std(img, axis=(0, 1)))

    avg = np.average(averages, axis=0)
    std = np.average(stds, axis=0)
    return avg, std


def histogram(img: Tensor):
    hist = [
        cv2.calcHist([img], [i], None, [256], [0, 256])
        for i, col in enumerate(('b', 'g', 'r'))
    ]
    return [
        _ / np.linalg.norm(_)
        for _ in hist
    ]


def img_stats(images: List[Tensor], filename: str):
    fig = plt.figure()

    shape = (len(images), 4)
    for i, img in enumerate(images):
        h = histogram(img)

        plot = fig.add_subplot(*shape, 4 * i + 1)
        plot.imshow(img[..., ::-1])
        for j, _ in enumerate(zip(['red', 'green', 'blue'], h)):
            plot = fig.add_subplot(*shape, 4 * i + 2 + j)
            plot.plot(_[1], color=_[0])
    plt.savefig(filename)
    plt.close(fig)
