import json

import numpy as np
from keras.callbacks import LearningRateScheduler
from keras.preprocessing.image import ImageDataGenerator

from hyper_search.train_parameters import TrainParameters
from mydeep_lib.callbacks import LRFinder
from mydeep_lib.dataframe import Dataframes
from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace


class SearchLearningRate(PipelineWorker):
    def __init__(self, train_params: TrainParameters, model_params: TrainParameters,
                 augmentation_params: TrainParameters) -> None:
        super().__init__('Learning Rate Finder', 'lr_finder')
        self.train_params = train_params
        self.model_params = model_params
        self.augmentation_params = augmentation_params

    def apply(self, target_ws: Workspace):
        dataset_ws = self.ctx.project_ws.get_ws('dataset')

        self.train_params.train_config()['lr'] = 1e-9

        # model ---------------------------------------
        model = self.model_params.build()
        model.compile(**self.train_params.train_config())

        # dataset -------------------------------------
        with open(dataset_ws.path_to('dataset.json')) as _:
            stats = json.load(fp=_)
        print(json.dumps(stats, indent=2, sort_keys=True))

        def prepare_dataset(name: str):
            dataset = Dataframes.from_csv(dataset_ws.path_to(name))
            dataset['id'] = dataset['id'].map('{}.tif'.format)
            return dataset

        train_df = prepare_dataset('train.csv').head(100000)
        test_df = prepare_dataset('test.csv').head(10)

        input_shape = model.get_layer(index=0).input_shape[1:-1]
        augmentation = ImageDataGenerator(**self.augmentation_params.params)
        train_gen = augmentation.flow_from_dataframe(train_df, x_col='id', y_col='label',
                                                     directory=stats['images_path'],
                                                     target_size=input_shape,
                                                     batch_size=self.train_params.params['batch_size'],
                                                     class_mode='categorical')
        test_gen = augmentation.flow_from_dataframe(test_df, x_col='id', y_col='label',
                                                    directory=stats['images_path'],
                                                    target_size=input_shape,
                                                    batch_size=self.ctx.max_batch_size,
                                                    class_mode='categorical')

        def step_decay_schedule(initial_lr=1e-3, decay_factor=0.75, step_size=10):
            def schedule(epoch):
                return initial_lr * (decay_factor ** np.floor(epoch / step_size))

            return LearningRateScheduler(schedule)

        batch_size = self.train_params.params['batch_size']
        lr_finder = LRFinder(
            min_lr=self.train_params.params['lr'],
            max_lr=1e-1,
            steps_per_epoch=np.ceil(len(train_df) / batch_size),
            epochs=self.train_params.params['epochs'])

        history = model.fit_generator(train_gen,
                                      epochs=1,
                                      validation_data=test_gen,
                                      verbose=1,
                                      callbacks=[
                                          lr_finder
                                          # step_decay_schedule(initial_lr=1e-4, decay_factor=0.75, step_size=2)
                                      ])
        lr_finder.plot_loss()
        lr_finder.plot_lr()

        return history
