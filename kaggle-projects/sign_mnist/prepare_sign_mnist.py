import os
from typing import Tuple

import numpy as np
import pandas as pd

from mydeep_lib.dataset import Dataset
from mydeep_lib.tensor_util import tensor_save, tensor_from_path
from sign_mnist.treshold_filter import extract_features
from stream_lib.stream import stream
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines_v2.worker import Worker
from surili_core.workspace import Workspace


def load_dataframe(csv_path: str, target_shape: Tuple[int, int]):
    _df = pd.read_csv(csv_path)
    y_col = 'label'
    labels = _df[y_col].values
    _df.drop(y_col, axis=1, inplace=True)
    images = [np.reshape(i, target_shape) for i in _df.values]
    # images = np.array([i.flatten() for i in images])
    return pd.DataFrame(data={'x': images, 'y': labels})


class ImageFileCreation(Worker):
    def run(self, ctx: PipelineContext, target_ws: Workspace):
        df = load_dataframe(
            csv_path=ctx.root_ws.path_to('sign_mnist_train.csv'),
            target_shape=(28, 28))

        target_path = target_ws.get_ws('images').path

        df['x'] = stream(df['x']) \
            .enumerate() \
            .map(lambda image: [name_provider(df)(image[0]), image[1]]) \
            .map(tensor_save(target_path)) \
            .map(os.path.basename) \
            .map(lambda _: os.path.splitext(_)[0]) \
            .to_list()

        dataset = Dataset(
            dataset=df,
            images_path=target_path,
            images_ext='jpg')
        dataset.to_path(target_ws.path_to('dataset.json'))

        return ctx


class FeatureFileCreation(Worker):

    def __init__(self, input_path: str):
        self.input_path = input_path

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        source_ws = ctx.project_ws.get_ws(self.input_path)
        target_path = target_ws.path_to('images')

        dataset = Dataset.from_path(source_ws.path_to('dataset.json'))
        df = dataset.df

        df['x'] = source_ws.get_ws('images') \
            .files \
            .map(tensor_from_path) \
            .map(extract_features) \
            .enumerate() \
            .map(lambda image: [name_provider(df)(image[0]), image[1]]) \
            .map(tensor_save(target_path)) \
            .map(os.path.basename) \
            .map(lambda _: os.path.splitext(_)[0]) \
            .to_list()

        dataset = Dataset(
            dataset=df,
            images_path=target_path,
            images_ext='jpg')
        dataset.to_path(target_ws.path_to('dataset.json'))

        return ctx


def name_provider(df: pd.DataFrame):
    def compute_name(index):
        label = df['y'][index]
        return 'cat{}_id{}'.format(label, index)

    return compute_name
