import numpy as np
import pandas as pd

from hyper_search.train_parameters import TrainParameters
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from mydeep_train.ctx.dataset import Dataset
from mydeep_train.ctx.train_dataset import TrainDataset
from mydeep_train.ctx.model import Model


class ComputeSubmission(PipelineWorker):
    def __init__(self, augmentation: TrainParameters, nb_pred: 1, target_x='x', target_y='y') -> None:
        super().__init__('compute submission', 'submission')
        self.augmentation = augmentation.build()
        self.nb_pred = nb_pred
        self.target_x = target_x
        self.target_y = target_y

    def apply(self, target_ws: Workspace):
        dataset = TrainDataset.from_path(self.ctx.project_ws.get_ws('dataset')).test
        self.make_predictions(dataset, target_ws)

    def make_predictions(self, dataset: Dataset, target_ws: Workspace):
        # model ---------------------------------------
        training_ws = self.ctx.project_ws.get_ws('training')
        model = Model.from_path(training_ws.path_to('output/model_final.h5'))

        df = dataset.df
        df['_filename'] = dataset.filenames()
        df = df.sort_values(by=[dataset.x_col])

        batch_size = self.ctx.max_batch_size
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

        return self.write_to_disk(x_values, y_values, target_ws.path_to('submission_from_{}.csv'.format(self.nb_pred)))

    def write_to_disk(self, x_values, y_values: np.ndarray, path: str):
        predictions = pd.DataFrame({
            self.target_x: x_values,
            self.target_y: y_values
        })
        predictions.to_csv(path, index=False)
        return predictions
