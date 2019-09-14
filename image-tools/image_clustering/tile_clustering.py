import glob
import os
from typing import List

import cv2
import numpy as np
from scipy.stats import wasserstein_distance
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline

from image_clustering.flag import Flag, FlagComputer
from image_clustering.tiler import Box, GridTiler
from mydeep_api.tensor import Tensor


class Params(object):
    def __init__(self, bins: int = 64, pca_components: int = 64, tile_size: int = 64):
        self.bins = bins
        self.pca_components = pca_components
        self.tiler = GridTiler(tile_size=tile_size)

    def compute_hist(self, img: Tensor):
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # h, _ = np.histogram(gray, bins=self.bins*3, range=[0, 256])
        # return h / np.linalg.norm(h)

        r, _ = np.histogram(img[2], bins=self.bins, range=[0, 256])
        r = r / np.linalg.norm(r)
        g, _ = np.histogram(img[1], bins=self.bins, range=[0, 256])
        g = g / np.linalg.norm(g)
        b, _ = np.histogram(img[0], bins=self.bins, range=[0, 256])
        b = b / np.linalg.norm(b)
        return np.hstack((r, g, b))


class Clusters(object):
    def __init__(self, path: str, p: Params):
        self.p = p
        self.path = path
        self.clusters = [
            [p.compute_hist(cv2.imread(img_path)) for img_path in glob.glob('{}/{}/*.png'.format(self.path, _))]
            for _ in os.listdir(path)
        ]

    def tag_computer(self, img: Tensor):
        def tag_computer(box: Box):
            hist = self.p.compute_hist(box.cut(img))

            d2 = [min([wasserstein_distance(hist, _) for _ in c]) for c in self.clusters]
            index2 = np.argmin(d2)
            return Flag.from_name(box, COLORS[index2])

        return tag_computer


def compute_clusters(p: Params, images: List[str], colors: List[str]):
    dataset = []
    for _ in images:
        img = cv2.imread(_)

        boxes = p.tiler.tiles(img.shape[:2])
        histograms = [p.compute_hist(_.cut(img)) for _ in boxes]
        dataset.extend(histograms)

    # pipeline = Pipeline(steps=[
    #     ('pca', PCA(n_components=p.pca_components)),
    #     ('clustering', BernoulliRBM(n_components=len(colors), random_state=0, verbose=True)),
    # ])
    pipeline = Pipeline(steps=[
        ('pca', PCA(n_components=p.pca_components)),
        ('clustering', AgglomerativeClustering(n_clusters=len(colors))),

        #     ('clustering', KMeans(n_clusters=len(colors), n_init=20)),
        #
        #     # ('clustering', GaussianMixture(n_components=len(colors), n_init=100)),
        #     # ('clustering', MiniBatchKMeans(n_clusters=len(colors), n_init=100)),
        #     # ('clustering', DBSCAN()),
        #     # ('clustering', MeanShift(bandwidth=2)),
        #     # ('clustering', SpectralClustering(n_clusters=len(colors), n_init=250)),
    ])

    # param_grid = {
    #     'pca__n_components': [3, 5, 8, 10, 15],
    # }
    # search = GridSearchCV(pipeline, param_grid, iid=False, cv=5)
    # search.fit(dataset)
    # print("Best parameter (CV score=%0.3f):" % search.best_score_)
    # print(search.best_params_)
    # results = pd.DataFrame(search.cv_results_)

    pipeline.fit(dataset)

    def tag_computer_provider(img: Tensor):
        def tag_computer(box: Box):
            hist = p.compute_hist(box.cut(img))

            # index = pipeline.predict([hist])[0]
            index = np.argmax(pipeline.transform([hist]))
            return Flag.from_name(box, colors[index])

        return tag_computer

    return tag_computer_provider


def tile_clustering(img: Tensor, flag_computer: FlagComputer, tiler: GridTiler):
    out = img.copy()
    tiles = [flag_computer(box) for box in tiler.tiles(img.shape[:2])]
    k = 4
    for tile in tiles:
        pt1 = (tile.box.left + k, tile.box.top + k)
        pt2 = (tile.box.right - k, tile.box.bottom - k)
        cv2.rectangle(out, pt1, pt2, tile.color)
    return out


def compute_std(paths: List[str]):
    averages = []
    stds = []
    for _ in images:
        img = cv2.imread(_)
        averages.append(np.average(img, axis=(0, 1)))
        stds.append(np.std(img, axis=(0, 1)))

    avg = np.average(averages, axis=0)
    std = np.average(stds, axis=0)
    return avg, std


COLORS = ['red', 'blue', 'green', 'white', 'yellow', 'orange', 'purple', 'cyan', 'magenta', 'gray']
P = Params(
    bins=64,
    pca_components=64,
    tile_size=32
)
CLUSTERS = Clusters('../image_editor/tiles', P)

if __name__ == '__main__':
    N = 1
    images = glob.glob('../tests/tiles/*_?.png')

    # avg, std = compute_std(images)
    # print('avg:' + str(avg))
    # print('std:' + str(std))

    tag_computer_provider = compute_clusters(P, images, COLORS[:5])
    os.makedirs('dataset', exist_ok=True)

    for _ in images:
        name = os.path.basename(_).replace('.tif', '')
        img = cv2.imread(_)

        img1 = tile_clustering(img, tag_computer_provider(img), P.tiler)
        cv2.imwrite('dataset/{}_model.png'.format(name), img1)

        # img2 = tile_clustering(img, CLUSTERS.tag_computer(img), P.tiler)
        # cv2.imwrite('dataset/{}_clusters.png'.format(name), img2)
