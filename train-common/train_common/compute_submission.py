import os
import numpy as np
import pandas as pd

from hyper_search.train_parameters import TrainParameters
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import TrainingDataset, Dataset
from train_common.ctx.model import Model


class ComputeSubmission(PipelineWorker):
    def __init__(self, augmentation: TrainParameters, nb_pred: 1, target_x='x', target_y='y') -> None:
        super().__init__('compute submission', 'submission')
        self.augmentation = augmentation.build()
        self.nb_pred = nb_pred
        self.target_x = target_x
        self.target_y = target_y

    def apply(self, target_ws: Workspace):
        # dataset -------------------------------------
        dataset = TrainingDataset.from_path(self.ctx.project_ws.get_ws('dataset')).test

        self.make_predictions(dataset, target_ws)

    def make_predictions(self, dataset: Dataset, target_ws: Workspace):
        # model ---------------------------------------
        training_ws = self.ctx.project_ws.get_ws('training')
        model = Model.from_path(training_ws.path_to('output/model_final.h5'))

        df = dataset.df
        df['_filename'] = dataset.filenames()
        df = df.sort_values(by=[dataset.x_col])

        batch_size = self.ctx.max_batch_size
        steps_number = dataset.steps_number(batch_size)

        generator = self.augmentation.flow_from_dataframe(
            dataframe=df,
            directory=dataset.img_path,
            x_col='_filename', y_col=dataset.y_col,
            target_size=model.input_shape(),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False)

        x_values = df[dataset.x_col]
        predictions = []
        for i in range(self.nb_pred):
            raw_predictions = model.keras_model.predict_generator(generator, steps=steps_number, verbose=1)
            labels = raw_predictions[:, 1]
            predictions.append(labels)
            self.write_to_disk(x_values, labels, target_ws.path_to('predictions_{}.csv'.format(i)))
        y_values = np.average(predictions, axis=0)
        self.write_to_disk(x_values, y_values, target_ws.path_to('submission_from_{}.csv'.format(self.nb_pred)))

        return pd.DataFrame({
            self.target_x: x_values,
            self.target_y: y_values
        })

    def write_to_disk(self, x_values, y_values: np.ndarray, path: str):
        predictions = pd.DataFrame({
            self.target_x: x_values,
            self.target_y: y_values
        })
        predictions.to_csv(path, index=False)
