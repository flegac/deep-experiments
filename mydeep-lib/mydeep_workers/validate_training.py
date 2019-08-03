import numpy as np
import pandas as pd

from hyper_search.train_parameters import TrainParameters
from mydeep_api._deprecated.file_dataset import FileDataset
from mydeep_api._deprecated.train_dataset import TrainDataset
from mydeep_api.monitoring.confusion_viewer import ConfusionViewer
from mydeep_api.monitoring.history_viewer import HistoryViewer
from mydeep_keras.k_model import KModel
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class ValidateTraining(Worker):
    def __init__(self, augmentation: TrainParameters, max_batch_size: int = 256) -> None:
        super().__init__()
        self.augmentation = augmentation.build()
        self.target_x = 'x'
        self.target_y = 'y'
        self.max_batch_size = max_batch_size

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        # training histogram -----------------------------------
        training_ws = target_ws.root.get_ws('training')
        history_viewer = HistoryViewer.from_path(training_ws.path_to('training_logs.csv'))
        history_viewer.save(target_ws.path_to('training.png'))

        # confusion matrix -------------------------------------
        dataset = TrainDataset.from_path(target_ws.root.get_ws('dataset')).test

        result = self.make_predictions(dataset, target_ws)

        # FIXME: this is not generic !
        # result[self.target_y] = result[self.target_y].apply(lambda x: 'n' + str(x))

        cm = ConfusionViewer(dataset.df[dataset.y_col], result[dataset.y_col])
        cm.save(target_ws.path_to('confusion_matrix'), normalize=True)
        cm.show()

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

    def make_predictions(self, dataset: FileDataset, target_ws: Workspace):
        # model ---------------------------------------
        training_ws = target_ws.root.get_ws('training')
        model = KModel.from_path(training_ws.path_to('output/model_final.h5'))

        df = dataset.df
        df['_filename'] = dataset.filenames()
        df = df.sort_values(by=[dataset.x_col])

        batch_size = self.max_batch_size
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
