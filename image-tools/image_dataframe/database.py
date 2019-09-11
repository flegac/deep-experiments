import glob
import os
import uuid

import cv2
import numpy as np
import pandas as pd
from more_itertools import flatten
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

from image_clustering.image_utils import contrast_stretching
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
    def build_row(row):
        x1 = row[1]['x1']
        x2 = row[1]['x2']
        y = row[1]['y']
        x_img1 = contrast_stretching(cv2.imread(x1))
        x_img2 = contrast_stretching(cv2.imread(x2))

        y_img = cv2.imread(y)

        return [
            (
                x1, x2, y,
                box.top, box.bottom, box.left, box.right,
                *np.average(np.hstack((box.cut(x_img1), box.cut(x_img2))), axis=(0, 1)),
                *np.std(np.hstack((box.cut(x_img1), box.cut(x_img2))), axis=(0, 1)),
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
        'avg_b', 'avg_g', 'avg_r',
        'std_b', 'std_g', 'std_r',
        'tagged'
    ])


tile_size = 64
df = tile_dataframe(
    df=df_from_path('../../feat-detection/detection/images'),
    tiler=GridTiler(tile_size=tile_size, stride=32)
)

dataset = df[['avg_b', 'avg_g', 'avg_r', 'std_b', 'std_g', 'std_r']]

n_clusters = 10

pipeline = Pipeline(steps=[
    # ('pca', PCA(n_components=64)),
    ('clustering', KMeans(n_clusters=n_clusters, n_init=20)),
])

pipeline.fit(dataset)

df['k'] = pipeline.predict(dataset)

for i in range(n_clusters):
    print('tiles[{}] : {}'.format(i, len(df[df.k == i][df.tagged > 0].values)))

for i in range(n_clusters):
    base = 'data/{}'.format(i)
    os.makedirs(base, exist_ok=True)

    for _ in df[df.k == i][df.tagged > 0].sample(n=50, replace=True).values:
        box = Box.from_limits(*_[3:7])
        img1 = box.cut(cv2.imread(_[0]))
        img2 = box.cut(cv2.imread(_[1]))
        img3 = box.cut(cv2.imread(_[2], cv2.IMREAD_COLOR)*255).astype('uint8')
        if img1.shape[:2] == (tile_size, tile_size):
            cv2.imwrite(os.path.join(base, str(uuid.uuid4()) + '.png'), np.hstack((img1, img2, img3)))
