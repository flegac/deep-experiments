from tqdm import tqdm

from mydeep_lib.tensor.tensor_util import tensor_save
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace

import pandas as pd

import numpy as np

from train_common.ctx.dataset import Dataset


class PrepareSignMnist(PipelineWorker):

    def __init__(self):
        super().__init__('Prepare raw dataset', 'raw_dataset')
        self.col_x = 'x'
        self.col_y = 'y'

    def apply(self, target_ws: Workspace):
        def load_dataframe(filename: str):
            _df = pd.read_csv(self.ctx.root_ws.path_to(filename))
            labels = _df['label'].values
            _df.drop('label', axis=1, inplace=True)
            images = [np.reshape(i, (28, 28)) for i in _df.values]
            # images = np.array([i.flatten() for i in images])
            return pd.DataFrame(data={'x': images, 'y': labels})

        training = load_dataframe('sign_mnist_train.csv')
        validation = load_dataframe('sign_mnist_test.csv')
        df = pd.concat([training, validation], axis=0, ignore_index=True)

        filenames = [0] * len(df)
        for i, image in tqdm(enumerate(df[self.col_x])):
            label = df[self.col_y][i]
            name = 'cat{}_id{}'.format(label, i)
            target_path = target_ws.get_ws('images').path
            tensor_save(target_path)([name, image])
            filenames[i] = name
        df[self.col_x] = filenames

        dataset = Dataset(
            dataset=df,
            images_path=target_ws.path_to('images'),
            images_ext='jpg')
        dataset.to_path(target_ws.path_to('dataset.json'))
