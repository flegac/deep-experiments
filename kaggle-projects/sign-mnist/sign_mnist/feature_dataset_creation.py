import os

from mydeep_api._deprecated.file_dataset import FileDataset
from sign_mnist.prepare_sign_mnist import name_provider
from sign_mnist.treshold_filter import extract_features
from stream_lib.stream import stream
from surili_core.surili_io.image_io import OpencvIO
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class FeatureDatasetCreation(Worker):

    def __init__(self, input_path: str):
        self.input_path = input_path

    def run(self, ws: Workspace):
        source_ws = ws.root.get_ws(self.input_path)
        image_ws = ws.get_ws('images')

        dataset = FileDataset.from_path(source_ws.path_to('dataset.json'))
        df = dataset.df

        df['x'] = stream(dataset.filenames()) \
            .map(OpencvIO().read) \
            .map(extract_features) \
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
