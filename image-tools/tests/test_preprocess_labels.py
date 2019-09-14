import glob
import os

import cv2
import numpy as np


def test_preprocess_labels():
    images = glob.glob('../../feat-detection/detection/images/*_mask.tif')

    os.makedirs('tiles', exist_ok=True)
    for _ in images:
        name = os.path.basename(_).replace('.tif', '')
        img = cv2.imread(_, cv2.IMREAD_GRAYSCALE) * 255
        cv2.imwrite('tiles/{}_before.jpg'.format(name), img)
        img = img_preprocessing(img)
        cv2.imwrite('tiles/{}_after.jpg'.format(name), img)

    # for _ in glob.glob('../../feat-detection/detection/images/*_?.tif'):
    #     name = os.path.basename(_).replace('.tif', '')
    #     img = cv2.imread(_)
    #     cv2.imwrite('tiles/{}.jpg'.format(name), img)


def img_preprocessing(img):
    # img = cv2.Canny(img, 100, 255)

    kernel3 = np.ones((5, 5), np.uint8)

    img = cv2.dilate(img, kernel3, iterations=1)

    img = cv2.dilate(img, kernel3, iterations=3)
    img = cv2.erode(img, kernel3, iterations=3)

    return img
