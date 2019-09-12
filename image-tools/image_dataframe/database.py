import glob
import os
import uuid

import cv2
import numpy as np
import pandas as pd
from joblib import dump, load
from more_itertools import flatten
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

from image_clustering.tiler import GridTiler, Box


def df_from_path(path: str):
    y = glob.glob('{}/*_mask.tif'.format(path))
    x1 = [_.replace('_mask.tif', '_0.tif') for _ in y]
    x2 = [_.replace('_mask.tif', '_1.tif') for _ in y]
    return pd.DataFrame({
        'x1': x1,
        'x2': x2,
        'y': y
    })


def tile_dataframe(df: pd.DataFrame, tiler: GridTiler):
    print('tiling ...')

    def build_row(row):
        x1 = row[1]['x1']
        x2 = row[1]['x2']
        y = row[1]['y']
        # f = lambda _: _
        # x_img1 = f(cv2.imread(x1))
        # x_img2 = f(cv2.imread(x2))

        y_img = cv2.imread(y)

        return [
            (
                x1, x2, y,
                box.top, box.bottom, box.left, box.right,
                # *np.average(np.hstack((box.cut(x_img1), box.cut(x_img2))), axis=(0, 1)),
                # *np.std(np.hstack((box.cut(x_img1), box.cut(x_img2))), axis=(0, 1)),
                (box.cut(y_img) == 1).sum()
            )
            for box in tiler.tiles(y_img.shape)
        ]

    rows = flatten([
        build_row(row)
        for row in df.iterrows()
    ])

    return pd.DataFrame(data=rows, columns=[
        'x1', 'x2', 'y',
        'top', 'bottom', 'left', 'right',
        # 'avg_b', 'avg_g', 'avg_r',
        # 'std_b', 'std_g', 'std_r',
        'tagged'
    ])


class ComputeColorStats(BaseEstimator, TransformerMixin):
    def fit(self, x, y=None):
        return self

    def transform(self, X, y=None, **fit_params):
        features = np.empty(shape=(len(X), 6), dtype=float)
        for i, x in enumerate(X):
            features[i] = (
                *np.average(x, axis=(0, 1)),
                *np.std(x, axis=(0, 1)),
            )
        return features

    def fit_transform(self, X, y=None, **fit_params):
        return self.transform(X, y, **fit_params)


class Clustering(object):
    def __init__(self, path: str, df: pd.DataFrame = None, n_clusters: int = 10):
        self.n_clusters = n_clusters
        self.path = path
        if os.path.exists(path):
            self.pipeline = load(path)
        else:
            self.pipeline = Pipeline(steps=[
                ('stats', ComputeColorStats()),
                ('clustering', KMeans(n_clusters=n_clusters, n_init=20)),
            ])
            self.fit(df)

    def predict(self, df: pd.DataFrame):
        print('predict ...')
        dataset = df.apply(self._extract_box, axis=1)
        return self.pipeline.predict(dataset)

    def fit(self, df: pd.DataFrame):
        print('fitting ...')
        dataset = df.apply(self._extract_box, axis=1)
        self.pipeline.fit(dataset)

    def save(self):
        dump(self.pipeline, self.path)

    @staticmethod
    def _extract_box(row):
        box = Box.from_limits(*row[3:7])
        x1 = cv2.imread(row[0])
        x2 = cv2.imread(row[1])
        return np.hstack((box.cut(x1), box.cut(x2)))


tile_size = 64
df = tile_dataframe(
    df=df_from_path('../../feat-detection/detection/images'),
    tiler=GridTiler(tile_size=tile_size, stride=32)
)

os.makedirs('data', exist_ok=True)

model = Clustering('data/model.joblib', df)
model.save()
df['k'] = model.predict(df)

for i in range(model.n_clusters):
    print('tiles[{}] : {}'.format(i, len(df[df.k == i][df.tagged > 0].values)))

for i in range(model.n_clusters):
    base = 'data/{}'.format(i)
    os.makedirs(base, exist_ok=True)

    for _ in df[df.k == i][df.tagged > 0].sample(n=50, replace=True).values:
        box = Box.from_limits(*_[3:7])
        img1 = box.cut(cv2.imread(_[0]))
        img2 = box.cut(cv2.imread(_[1]))
        img3 = box.cut(cv2.imread(_[2], cv2.IMREAD_COLOR) * 255).astype('uint8')
        if img1.shape[:2] == (tile_size, tile_size):
            cv2.imwrite(os.path.join(base, str(uuid.uuid4()) + '.png'), np.hstack((img1, img2, img3)))
