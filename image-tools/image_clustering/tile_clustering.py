import glob
import os
from typing import List, Callable

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from scipy.stats import wasserstein_distance
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline

from image_clustering.tiler import GridTiler
from mydeep_api.tensor import Tensor

TagComputer = Callable[[Tensor], int]
HistComputer = Callable[[Tensor], Tensor]


class Params(object):
    def __init__(self, bins: int = 64, pca_components: int = 64, tile_size: int = 64):
        self.bins = bins
        self.pca_components = pca_components
        self.tiler = GridTiler(tile_size=tile_size)

    def hist_computer(self, img: Tensor):
        r, _ = np.histogram(img[2], bins=self.bins, range=[0, 256])
        r, _ = np.histogram(img[2], bins=self.bins, range=[0, 256])
        r = r / np.linalg.norm(r)
        g, _ = np.histogram(img[1], bins=self.bins, range=[0, 256])
        g = g / np.linalg.norm(g)
        b, _ = np.histogram(img[0], bins=self.bins, range=[0, 256])
        b = b / np.linalg.norm(b)
        return np.hstack((r, g, b))


class ClusterTagComputer(TagComputer):
    def __init__(self, path: str, hist_computer: HistComputer):
        self.hist_computer = hist_computer
        self.clusters = [
            [hist_computer(cv2.imread(img_path)) for img_path in glob.glob('{}/{}/*.png'.format(path, _))]
            for _ in os.listdir(path)
        ]
        self.stats()

    def stats(self):
        for _ in self.clusters:
            for c in _:
                bins = np.array(range(len(c)))
                prob = c / np.sum(c)
                image = np.sort(np.random.choice(bins, size=128 * 128, replace=True, p=prob)).reshape((128, 128))
                plt.imshow(image, 'gray')

    def __call__(self, data: Tensor):
        hist = self.hist_computer(data)
        d2 = [min([wasserstein_distance(hist, _) for _ in c]) for c in self.clusters]
        return int(np.argmin(d2))


class KmeanTagComputer(TagComputer):
    def __init__(self, p: Params, images: List[str], cluster_number: int):
        self.hist_computer = p.hist_computer
        self.model = KMeans(n_clusters=cluster_number, n_init=20)

        dataset = []
        for _ in images:
            img = cv2.imread(_)
            boxes = GridTiler(tile_size=32).tiles(img.shape[:2])
            histograms = [p.hist_computer(box.cut(img)) for box in boxes]
            dataset.extend(histograms)

        self.pipeline = Pipeline(steps=[
            ('pca', PCA(n_components=p.pca_components)),
            ('clustering', self.model),
        ])
        self.pipeline.fit(dataset)
        # self.stats()

    def stats(self):
        centers = (self.model.cluster_centers_ + 1) / 2
        for c in centers:
            bins = np.array(range(len(c))) * 4
            prob = c / np.sum(c)
            image = np.sort(np.random.choice(bins, size=128 * 128, replace=True, p=prob)).reshape((128, 128))
            plt.imshow(image, 'gray')

    def __call__(self, data: Tensor):
        hist = self.hist_computer(data)
        return self.pipeline.predict([hist])[0]


def tile_clustering(img: Tensor, tag_computer: TagComputer, tiler: GridTiler):
    out = img.copy()
    k = 8
    for box in tiler.tiles(img.shape[:2]):
        flag = tag_computer(box.cut(img))
        pt1 = (box.left + k, box.top + k)
        pt2 = (box.right - k, box.bottom - k)
        cv2.rectangle(out, pt1, pt2, tuple(256 * _ for _ in to_rgb(COLORS[flag])), 2)
    return out


COLORS = ['red', 'blue', 'green', 'white', 'yellow',
          'orange', 'purple', 'cyan', 'magenta', 'gray']
P = Params(
    bins=128,
    pca_components=128,
    tile_size=128
)

if __name__ == '__main__':
    dataset = 'cs'
    images = glob.glob('../tests/20190802_export_s2_it1/{}/*_?.png'.format(dataset))

    model_tag_computer = KmeanTagComputer(P, images, cluster_number=4)
    cluster_tag_computer = ClusterTagComputer('../image_editor/tiles', P.hist_computer)

    os.makedirs(dataset, exist_ok=True)
    for _ in images:
        name = os.path.basename(_).replace('.tif', '')
        img = cv2.imread(_)

        img1 = tile_clustering(img, model_tag_computer, P.tiler)
        cv2.imwrite('{}/{}_model.png'.format(dataset, name), img1)

        # img2 = tile_clustering(img, cluster_tag_computer, P.tiler)
        # cv2.imwrite('{}/{}_clusters.png'.format(dataset, name), img2)
