import os
from typing import Tuple

import numpy as np
import pandas as pd

from mydeep_api._deprecated.file_dataset import FileDataset
from sign_mnist.prepare_sign_mnist import name_provider
from stream_lib.stream import stream
from surili_core.surili_io.image_io import OpencvIO
from surili_core.worker import Worker
from surili_core.workspace import Workspace


def load_dataframe(csv_path: str, target_shape: Tuple[int, int]):
    _df = pd.read_csv(csv_path)
    y_col = 'label'
    labels = _df[y_col].values
    _df.drop(y_col, axis=1, inplace=True)
    images = [np.reshape(i, target_shape) for i in _df.values]
    # images = np.array([i.flatten() for i in images])
    return pd.DataFrame(data={'x': images, 'y': labels})


class RawDatasetCreation(Worker):
    def __init__(self, train_csv_path: str):
        self.train_csv_path = train_csv_path

    def run(self, ws: Workspace):
        df = load_dataframe(
            csv_path=ws.root.path_to(self.train_csv_path),
            target_shape=(28, 28))

        image_ws = ws.get_ws('images')

        df['x'] = stream(df['x']) \
            .enumerate() \
            .map(lambda image: [image_ws.path_to(name_provider(df)(image[0])), image[1]]) \
            .map(OpencvIO().write) \
            .map(os.path.basename) \
            .map(lambda _: os.path.splitext(_)[0]) \
            .to_list()

        FileDataset(
            dataset=df,
            image_path_template=image_ws.path_to('{}.jpg')
        ).to_path(ws.path_to('dataset.json'))
