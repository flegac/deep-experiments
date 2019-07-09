import numpy as np
import pandas as pd

from hyper_search.train_parameters import TrainParameters
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace
from mydeep_lib.dataset import Dataset
from mydeep_lib.train_dataset import TrainDataset
from mydeep_keras.k_model import KModel


class ComputeSubmission(Worker):
    def __init__(self, augmentation: TrainParameters, nb_pred: 1, target_x='x', target_y='y') -> None:
        super().__init__('compute submission', 'submission')
        self.augmentation = augmentation.build()
        self.nb_pred = nb_pred
        self.target_x = target_x
        self.target_y = target_y

    def apply(self, ctx: PipelineContext, target_ws: Workspace):
        dataset = TrainDataset.from_path(ctx.project_ws.get_ws('dataset')).test
        self.make_predictions(ctx, dataset, target_ws)

    def make_predictions(self, ctx: PipelineContext, dataset: Dataset, target_ws: Workspace):
        # model ---------------------------------------
        training_ws = ctx.project_ws.get_ws('training')
        model = KModel.from_path(training_ws.path_to('output/model_final.h5'))

        df = dataset.df
        df['_filename'] = dataset.filenames()
        df = df.sort_values(by=[dataset.x_col])

        batch_size = ctx.max_batch_size
        input_shape = model.input_shape()

        x_values = df[dataset.x_col]
        predictions = []
        for i in range(self.nb_pred):
            raw_predictions = model.keras_model.predict_generator(
                generator=dataset.prepare_generator(batch_size, input_shape, self.augmentation, shuffle=False),
                steps=dataset.steps_number(batch_size),
                verbose=1)

            # FIXME: this is not generic !
            labels = raw_predictions[:, 1]

            predictions.append(labels)
            self.write_to_disk(x_values, labels, target_ws.path_to('predictions_{}.csv'.format(i)))

        y_values = np.average(predictions, axis=0)

        return self.write_to_disk(x_values, y_values,
                                  target_ws.path_to('submission_from_{}.csv'.format(self.nb_pred)))

    def write_to_disk(self, x_values, y_values: np.ndarray, path: str):
        predictions = pd.DataFrame({
            self.target_x: x_values,
            self.target_y: y_values
        })
        predictions.to_csv(path, index=False)
        return predictions
