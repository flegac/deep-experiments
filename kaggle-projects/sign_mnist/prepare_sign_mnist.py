from typing import Tuple

from tqdm import tqdm

from mydeep_lib.tensor.tensor_util import tensor_save, tensor_from_path
from mydeep_train.ctx.dataset import Dataset
from sign_mnist.treshold_filter import extract_features
from surili_core.pipeline_context import PipelineContext
from surili_core.workspace import Workspace

import pandas as pd

import numpy as np


def load_dataframe(csv_path: str, target_shape: Tuple[int, int]):
    _df = pd.read_csv(csv_path)
    y_col = 'label'
    labels = _df[y_col].values
    _df.drop(y_col, axis=1, inplace=True)
    images = [np.reshape(i, target_shape) for i in _df.values]
    # images = np.array([i.flatten() for i in images])
    return pd.DataFrame(data={'x': images, 'y': labels})


def sign_mnist_preparator(ctx: PipelineContext, target_ws: Workspace):
    col_x = 'x'
    col_y = 'y'

    df = load_dataframe(
        csv_path=ctx.root_ws.path_to('sign_mnist_train.csv'),
        target_shape=(28, 28))
    filenames = [0] * len(df)
    for i, image in tqdm(enumerate(df[col_x])):
        label = df[col_y][i]
        name = 'cat{}_id{}'.format(label, i)
        target_path = target_ws.get_ws('images').path
        # image = extract_features(image)
        tensor_save(target_path)([name, image])
        filenames[i] = name
    df[col_x] = filenames

    dataset = Dataset(
        dataset=df,
        images_path=target_ws.path_to('images'),
        images_ext='jpg')
    dataset.to_path(target_ws.path_to('dataset.json'))

    ctx.project_ws \
        .get_ws('dataset/images') \
        .files() \
        .map(tensor_from_path) \
        .map(extract_features) \
        .enumerate() \
        .foreach(tensor_save(target_ws.path_to('images')))

    return ctx
