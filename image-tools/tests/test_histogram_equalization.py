import glob
import os

import cv2

from image_clustering.image_utils import contrast_stretching


def test_hist_equalizer():
    images = glob.glob('../../feat-detection/detection/images/*_?.tif')

    os.makedirs('tiles', exist_ok=True)
    for _ in images:
        name = os.path.basename(_).replace('.tif', '')
        img = cv2.imread(_)
        img = img_preprocessing(img)
        cv2.imwrite('tiles/{}.png'.format(name), img)
        # cv2.imwrite('tiles/{}_corrected.png'.format(name), img)


def img_preprocessing(img):
    img = contrast_stretching(img)

    band = 1
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv[:, :, band] = cv2.equalizeHist(hsv[:, :, band])
    hist_equalization_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return hist_equalization_result
