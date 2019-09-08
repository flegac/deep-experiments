import glob
import os
from pathlib import Path

import cv2
import numpy as np
from skimage import img_as_float
from skimage import transform
from skimage.measure import compare_ssim as ssim

# Histogram of Oriented Gradients
# https://www.learnopencv.com/histogram-of-oriented-gradients/
from image_clustering.image_utils import contrast_stretching, adaptive_equalization


# structural similarity
# histogram matching
# http://paulbourke.net/miscellaneous/equalisation/


def detection(x1, x2, win_size=1, power=2, treshold=.5):
    x1 = img_as_float(x1)
    x2 = img_as_float(x2)

    w, h, _ = x1.shape
    s, out = ssim(x1, x2, win_size=2 * win_size + 1, multichannel=True, full=True)
    mask = (np.average(1 - out, axis=2) ** power)
    return mask
    # return (mask > treshold).astype(mask.dtype)


def im_resize(img, scale):
    width = int(img.shape[1] * scale)
    height = int(img.shape[0] * scale)
    dim = (width, height)
    # resize image
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


def do_all(name, label, x1, x2, equalizer=None):
    if equalizer:
        x1 = equalizer(x1)
        x2 = equalizer(x2)

    cv2.imwrite('{}_{}_x1.png'.format(name, label), im_resize(x1, 2.))
    cv2.imwrite('{}_{}_x2.png'.format(name, label), im_resize(x2, 2.))
    y_pred = detection(x1, x2)
    cv2.imwrite('{}_y_pred_{}.png'.format(name, label), im_resize(y_pred, 2.) * 255)


def main():
    path = os.path.abspath(os.path.join(os.curdir, 'images'))

    dataset = glob.glob(os.path.join(path, '*_mask.tif'))

    for _ in dataset:
        name = Path(_).name.replace('_mask.tif', '')
        x1 = cv2.imread(_.replace('_mask.tif', '_0.tif'))
        x2 = cv2.imread(_.replace('_mask.tif', '_1.tif'))
        y = cv2.imread(os.path.join(_), cv2.IMREAD_GRAYSCALE)
        cv2.imwrite('{}_x1.png'.format(name), im_resize(x1, 2.))
        cv2.imwrite('{}_x2.png'.format(name), im_resize(x2, 2.))
        cv2.imwrite('{}_y.png'.format(name), im_resize(y, 2.) * 255)

        x1 = transform.match_histograms(x1, x2, multichannel=True)

        do_all(name, 'basic', x1, x2)
        do_all(name, 'stretch', x1, x2, contrast_stretching)
        do_all(name, 'adapt_eq', x1, x2, adaptive_equalization)


if __name__ == "__main__":
    main()
