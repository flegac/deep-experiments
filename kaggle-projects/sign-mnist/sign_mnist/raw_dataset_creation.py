import os
from typing import Tuple

import numpy as np
import pandas as pd

from mydeep_api._deprecated.file_dataset import FileDataset
from sign_mnist.prepare_sign_mnist import name_provider
from stream_lib.stream import stream
from surili_core.pipeline_context import PipelineContext
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
    def run(self, ctx: PipelineContext, target_ws: Workspace):
        df = load_dataframe(
            csv_path=ctx.root_ws.path_to('sign_mnist_train.csv'),
            target_shape=(28, 28))

        image_ws = target_ws.get_ws('images')

        df['x'] = stream(df['x']) \
            .enumerate() \
            .map(lambda image: [image_ws.path_to(name_provider(df)(image[0])), image[1]]) \
            .map(OpencvIO().save) \
            .map(os.path.basename) \
            .map(lambda _: os.path.splitext(_)[0]) \
            .to_list()

        FileDataset(
            dataset=df,
            image_path_template=image_ws.path_to('{}.jpg')
        ).to_path(target_ws.path_to('dataset.json'))

        return ctx
