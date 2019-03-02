import numpy as np

from mydeep_lib.callbacks.lr_finder import LRFinder
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.train_context import TrainContext
from train_common.ctx.train_dataset import TrainDataset


class SearchLearningRate(PipelineWorker):
    def __init__(self, params: TrainContext, min_lr: float = 1e-6, max_lr: float = 1., epochs=2) -> None:
        super().__init__('Learning Rate Finder', 'lr_finder')
        self.params = params
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.epochs = epochs

    def apply(self, target_ws: Workspace):
        dataset_ws = self.ctx.project_ws.get_ws('dataset')

        # load params
        dataset = TrainDataset.from_path(dataset_ws)
        model = self.params.model
        train_params = self.params.params
        train_augmentation = self.params.augmentation.build()

        # ----- lr search ----------------------------------------------------------
        batch_size = train_params.params['batch_size']
        input_shape = model.input_shape()

        lr_finder = LRFinder(
            min_lr=self.min_lr,
            max_lr=self.max_lr,
            steps_per_epoch=dataset.train.steps_number(batch_size),
            epochs=self.epochs)

        history = model.keras_model.fit_generator(
            dataset.train.prepare_generator(batch_size, input_shape, train_augmentation),
            steps_per_epoch=dataset.train.steps_number(batch_size),
            epochs=self.epochs,
            verbose=1,
            callbacks=[
                lr_finder
            ])
        fig = lr_finder.plot_loss()
        fig.savefig(target_ws.path_to('learning_rate.png'))
        fig.show()

        return history
