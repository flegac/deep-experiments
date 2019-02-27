import os
import numpy as np
import pandas as pd
from pandas.core import series

from hyper_search.train_parameters import TrainParameters
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import Dataset, TrainingDataset
from mydeep_lib.visualize.confusion_matrix import ConfusionMatrix
from train_common.ctx.model import Model


class ValidateTraining(PipelineWorker):
    def __init__(self, augmentation: TrainParameters) -> None:
        super().__init__('Validate training', 'validation')
        self.augmentation = augmentation.build()
        self.x = 'x'
        self.y = 'y'

    def apply(self, target_ws: Workspace):
        # dataset -------------------------------------
        dataset = TrainingDataset.from_path(self.ctx.project_ws.get_ws('dataset'))

        result = self.make_predictions(dataset.test, target_ws)
        # result = Dataframes.from_csv(target_ws.path_to('submission_from_10.csv'))
        # result['prediction'] = result[self.y].apply(lambda x: 1 if x > .5 else 0)

        cm = ConfusionMatrix(dataset.test.df[self.y], result[self.y])
        cm.show(classes=list(dataset.test.df[self.y].unique()), normalize=True)

        errors = result[dataset.test.df[self.y] != result[self.y]]
        errors.to_csv(target_ws.path_to('errors.csv'), index=False)

        for category in list(errors[self.y].unique()):
            errors[errors[self.y] == category].to_csv(target_ws.path_to('errors_{}.csv'.format(category)), index=False)

        # TODO : compute correct predictions with low confidence (= doubtful results)
        # for doubt in [0.05, 0.1, 0.25, 0.333]:
        #     doubtful = result[abs(result[self.y] - .5) < doubt]
        #     doubtful.to_csv(target_ws.path_to('doubtful_{}.csv'.format(doubt)), index=False)

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
        pred = model.keras_model.predict_generator(generator, steps=steps_number, verbose=1)
        labels = pd.DataFrame(pred).apply(np.argmax, axis=1).apply(lambda x: 'n' + str(x)).values
        self.write_to_disk(labels, filenames, dataset.img_ext, target_ws.path_to('predictions.csv'))
        return pd.DataFrame({
            self.x: df[self.x],
            self.y: labels
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
