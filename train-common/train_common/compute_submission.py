import os
import numpy as np
import pandas as pd

from hyper_search.train_parameters import TrainParameters
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import TrainingDataset, Dataset
from train_common.ctx.model import Model


class ComputeSubmission(PipelineWorker):
    def __init__(self, augmentation: TrainParameters, nb_pred: 1) -> None:
        super().__init__('compute submission', 'submission')
        self.augmentation = augmentation.build()
        self.nb_pred = nb_pred
        self.x = 'x'
        self.y = 'y'

    def apply(self, target_ws: Workspace):
        # dataset -------------------------------------
        dataset = TrainingDataset.from_path(self.ctx.project_ws.get_ws('dataset'))

        self.make_predictions(dataset.test, target_ws)

    def make_predictions(self, dataset: Dataset, target_ws: Workspace):
        # model ---------------------------------------
        training_ws = self.ctx.project_ws.get_ws('training')
        model = Model.from_path(training_ws.path_to('output/model_final.h5'))

        df = dataset.df
        df['filename'] = df[self.x].apply(lambda x: '{}.{}'.format(x, dataset.img_ext))
        df = df.sort_values(by=[self.x])

        batch_size = self.ctx.max_batch_size
        steps_number = dataset.steps_number(batch_size)

        generator = self.augmentation.flow_from_dataframe(
            dataframe=df,
            directory=dataset.img_path,
            x_col='filename', y_col=self.y,
            target_size=model.input_shape(),
            batch_size=batch_size,
            class_mode='categorical',
            shuffle=False)

        filenames = df['filename']
        predictions = []
        for i in range(self.nb_pred):
            pred = model.keras_model.predict_generator(generator, steps=steps_number, verbose=1)
            labels = pred[:, 1]
            predictions.append(labels)
            self.write_to_disk(labels, filenames, dataset.img_ext, target_ws.path_to('predictions_{}.csv'.format(i)))
        final_labels = np.average(predictions, axis=0)
        self.write_to_disk(final_labels, filenames, dataset.img_ext,
                           target_ws.path_to('submission_from_{}.csv'.format(self.nb_pred)))
        return pd.DataFrame({
            self.x: dataset[self.x],
            self.y: final_labels
        })

    def write_to_disk(self, labels: np.ndarray, filenames, img_ext: str, path: str):
        predictions = pd.DataFrame({
            self.x: filenames,
            self.y: labels
        })
        predictions[self.x] = predictions[self.x] \
            .apply(os.path.basename) \
            .apply(lambda x: x.replace('.{}'.format(img_ext), ''))
        predictions.to_csv(path, index=False)
