import os

from mydeep_lib.dataset import Dataset
from mydeep_lib.tensor_util import tensor_from_path, tensor_save
from sign_mnist.prepare_sign_mnist import name_provider
from sign_mnist.treshold_filter import extract_features
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines_v2.worker import Worker
from surili_core.workspace import Workspace


class FeatureFileCreation(Worker):

    def __init__(self, input_path: str):
        self.input_path = input_path

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        source_ws = ctx.project_ws.get_ws(self.input_path)
        target_path = target_ws.path_to('images')

        dataset = Dataset.from_path(source_ws.path_to('dataset.json'))
        df = dataset.df

        filenames = dataset.filenames()

        df['x'] = source_ws.get_ws('images') \
            .files \
            .map(tensor_from_path) \
            .map(extract_features) \
            .enumerate() \
            .map(lambda image: [name_provider(df)(image[0]), image[1]]) \
            .map(tensor_save(target_path, no_overwrite=True)) \
            .map(os.path.basename) \
            .map(lambda _: os.path.splitext(_)[0]) \
            .to_list()

        Dataset(
            dataset=df,
            image_path_template=os.path.join(target_path, '{}.jpg')
        ).to_path(target_ws.path_to('dataset.json'))

        return ctx
