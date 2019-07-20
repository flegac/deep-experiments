from keras.preprocessing.image import ImageDataGenerator

from mydeep_api._deprecated.dataset import Dataset
from mydeep_api._deprecated.train_dataset import TrainDataset
from mydeep_keras.callbacks.lr_finder import LRFinder
from mydeep_keras.k_model import KModel
from mydeep_keras.k_train_context import KTrainContext
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class SearchLearningRate(Worker):
    def __init__(self, params: KTrainContext, min_lr: float = 1e-6, max_lr: float = 1., epochs: int = 2) -> None:
        super().__init__()
        self.params = params
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.epochs = epochs

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        dataset_ws = ctx.project_ws.get_ws('dataset')

        # load params
        dataset = TrainDataset.from_path(dataset_ws).train
        model = self.params.model
        train_params = self.params.params
        augmentation = self.params.augmentation.build()

        # ----- lr search ----------------------------------------------------------
        batch_size = train_params.params['batch_size']
        lr_finder = LRFinder(
            min_lr=self.min_lr,
            max_lr=self.max_lr,
            steps_per_epoch=dataset.steps_number(batch_size),
            epochs=self.epochs)

        history = model.keras_model.fit_generator(
            dataset.prepare_generator(batch_size, model.input_shape(), augmentation),
            steps_per_epoch=dataset.steps_number(batch_size),
            epochs=self.epochs,
            verbose=1,
            callbacks=[
                lr_finder
            ])
        fig = lr_finder.plot_loss()
        fig.savefig(target_ws.path_to('learning_rate.png'))
        fig.show()

        return history


def search_lr(model: KModel,
              dataset: Dataset,
              augmentation: ImageDataGenerator,
              min_lr: float = 1e-6,
              max_lr: float = 1.,
              epochs: int = 2,
              batch_size=64
              ):
    lr_finder = LRFinder(
        min_lr=min_lr,
        max_lr=max_lr,
        steps_per_epoch=dataset.steps_number(batch_size),
        epochs=epochs)

    history = model.keras_model.fit_generator(
        generator=dataset.prepare_generator(batch_size, model.input_shape(), augmentation),
        steps_per_epoch=dataset.steps_number(batch_size),
        epochs=epochs,
        verbose=1,
        callbacks=[
            lr_finder
        ])
    fig = lr_finder.plot_loss()
    fig.show()
    return history
