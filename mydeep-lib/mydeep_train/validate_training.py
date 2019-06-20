import os
import numpy as np
import pandas as pd

from hyper_search.train_parameters import TrainParameters
from mydeep_lib.visualize.visualize import Visualize
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from mydeep_train.ctx.dataset import Dataset
from mydeep_train.ctx.train_dataset import TrainDataset
from mydeep_lib.visualize.confusion_matrix import ConfusionMatrix
from mydeep_train.ctx.model import Model


class ValidateTraining(PipelineWorker):
    def __init__(self, augmentation: TrainParameters) -> None:
        super().__init__('Validate training', 'validation')
        self.augmentation = augmentation.build()
        self.target_x = 'x'
        self.target_y = 'y'

    def apply(self, target_ws: Workspace):
        # training histogram -----------------------------------
        training_ws = self.ctx.project_ws.get_ws('training')
        fig = Visualize.history_from_path(training_ws.path_to('training_logs.csv'))
        fig.savefig(target_ws.path_to('training.png'))

        # confusion matrix -------------------------------------
        dataset = TrainDataset.from_path(self.ctx.project_ws.get_ws('dataset')).test

        result = self.make_predictions(dataset, target_ws)

        # FIXME: this is not generic !
        # result[self.target_y] = result[self.target_y].apply(lambda x: 'n' + str(x))

        cm = ConfusionMatrix(dataset.df[dataset.y_col], result[dataset.y_col])
        fig = cm.plot(normalize=True)
        fig.savefig(target_ws.path_to('confusion_matrix'))
        fig.show()

        errors = result[dataset.df[dataset.y_col] != result[dataset.y_col]]
        errors.to_csv(target_ws.path_to('errors.csv'), index=False)
        y_classes = list(dataset.df[dataset.y_col].unique())

        for category in y_classes:
            errors_path = target_ws.path_to('errors_{}.csv'.format(category))
            errors[errors[dataset.y_col] == category].to_csv(errors_path, index=False)

        # TODO : compute correct predictions with low confidence (= doubtful results)
        # for doubt in [0.05, 0.1, 0.25, 0.333]:
        #     doubtful = result[abs(result[self.y] - .5) < doubt]
        #     doubtful.to_csv(target_ws.path_to('doubtful_{}.csv'.format(doubt)), index=False)

    def make_predictions(self, dataset: Dataset, target_ws: Workspace):
        # model ---------------------------------------
        training_ws = self.ctx.project_ws.get_ws('training')
        model = Model.from_path(training_ws.path_to('output/model_final.h5'))

        df = dataset.df
        df['_filename'] = dataset.filenames()
        df = df.sort_values(by=[dataset.x_col])

        batch_size = self.ctx.max_batch_size
        input_shape = model.input_shape()

        raw_predictions = model.keras_model.predict_generator(
            generator=dataset.prepare_generator(batch_size, input_shape, self.augmentation, shuffle=False),
            steps=dataset.steps_number(batch_size),
            verbose=1)

        predictions = pd.DataFrame({
            self.target_x: df[dataset.x_col],
            self.target_y: pd.DataFrame(raw_predictions)
                .apply(np.argmin, axis=1)
                .values
        })
        predictions.to_csv(target_ws.path_to('test_predictions.csv'), index=False)
        return predictions
