import cv2
import numpy as np

new_image = np.random.rand(3, 256, 256)
new_image[:, :, :] *= 255
new_image = new_image.astype(np.uint8)

cv2.imshow('my_image', np.dstack(new_image))
cv2.waitKey(0)
