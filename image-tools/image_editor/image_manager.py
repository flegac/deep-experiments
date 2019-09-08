import os
import uuid

import cv2
import matplotlib.pyplot as plt

from image_clustering.image_utils import contrast_stretching
from image_clustering.tiler import Box


class ImageManager(object):
    def __init__(self, image_path: str):
        self.name = os.path.basename(image_path).replace('.tif', '')
        self.image_path = image_path
        self.wind_id = os.path.basename(image_path)
        self.tile_centers = []
        self.source = cv2.imread(self.image_path)

        self.base = self.source.copy()
        self.current = self.base.copy()

        self.tile_size = (16, 16)

        self.mouse_pos = None
        self.is_running = False

    def stop(self):
        self.is_running = False

    def start(self):
        self.is_running = True
        cv2.namedWindow(self.wind_id)
        cv2.setMouseCallback(self.wind_id, self.mouse_listener)

        while self.is_running:
            cv2.imshow(self.wind_id, self.current)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('q'):
                self.stop()

            if key == ord('c'):
                self.base = contrast_stretching(self.source)

            if key == ord('h'):
                plt.hist(self.source.ravel(), 256, [0, 256])
                plt.show()

            if key == ord("r"):
                self.reset()

            if key == ord('s'):
                os.makedirs('tiles', exist_ok=True)

                count = len(os.listdir('tiles'))
                for i, _ in enumerate(self.tile_centers):
                    pt0 = _[1] - self.tile_size[1], _[0] - self.tile_size[0]
                    box = Box(*pt0, self.tile_size[1] * 2, self.tile_size[0] * 2)
                    tile = box.cut(self.source)

                    file_path = 'tiles/{}_{}'.format(self.name, count)
                    os.makedirs(file_path, exist_ok=True)
                    cv2.imwrite('{}/{}.png'.format(file_path, str(uuid.uuid4())), tile)
                self.reset()
        cv2.destroyWindow(self.wind_id)

    def reset(self):
        self.base = self.source.copy()
        self.tile_centers.clear()
        self.redraw()

    def mouse_listener(self, event, x, y, flags, param):
        self.mouse_pos = (x, y)

        if event == cv2.EVENT_LBUTTONDOWN:
            self.tile_centers.append((x, y))
        elif event == cv2.EVENT_LBUTTONUP:
            pass

        if event == cv2.EVENT_RBUTTONDOWN:
            pass
        elif event == cv2.EVENT_RBUTTONUP:
            pass
        self.redraw()

    def redraw_refs(self):
        for _ in self.tile_centers:
            pt0 = _[0] - self.tile_size[0], _[1] - self.tile_size[1]
            pt1 = _[0] + self.tile_size[0], _[1] + self.tile_size[1]
            cv2.rectangle(self.current, pt0, pt1, (0, 255, 0))
        pt0 = self.mouse_pos[0] - self.tile_size[0], self.mouse_pos[1] - self.tile_size[1]
        pt1 = self.mouse_pos[0] + self.tile_size[0], self.mouse_pos[1] + self.tile_size[1]
        cv2.rectangle(self.current, pt0, pt1, (0, 255, 255))

    def redraw(self):
        self.current = self.base.copy()
        self.redraw_refs()

    @property
    def selected_tiles(self):
        tiles = []
        for _ in self.tile_centers:
            pt0 = _[0] - self.tile_size[0], _[1] - self.tile_size[1]
            pt1 = _[0] + self.tile_size[0], _[1] + self.tile_size[1]
            tile = self.source[pt0[0]:pt1[0], pt0[1]:pt1[1]]
            tiles.append(tile)
        return tiles
