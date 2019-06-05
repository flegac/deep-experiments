from keras.callbacks import ModelCheckpoint, CSVLogger, Callback
from keras import backend as K

from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.train_dataset import TrainDataset
from train_common.ctx.train_context import TrainContext


class TrainerNoDeep(PipelineWorker):
    def __init__(self, params: TrainContext) -> None:
        super().__init__('model training', 'training')
        self.params = params

    def apply(self, target_ws: Workspace):
        dataset_ws = self.ctx.project_ws.get_ws('dataset')
        models_ws = target_ws.get_ws('models')
        params_ws = target_ws.get_ws('params')

        # load params
        dataset = TrainDataset.from_path(dataset_ws)
        model = self.params.model
        train_params = self.params.params
        train_augmentation = self.params.augmentation.build()
        test_augmentation = self.params.augmentation.build()

        #  save params
        with open(params_ws.path_to('params.json'), 'w') as _:
            _.write(str(train_params))
        with open(params_ws.path_to('augmentation.json'), 'w') as _:
            _.write(str(self.params.augmentation))
        model.to_path(params_ws.path_to('model.h5'))
        dataset.to_path(params_ws.get_ws('dataset'))

        # ----- training -------------------------------------------------------------
        batch_size = train_params.params['batch_size']
        input_shape = model.input_shape()

        print(dataset.train.df.head(2))
        print(dataset.test.df.head(2))

        history = model.keras_model.fit_generator(
            generator=dataset.train.prepare_generator(batch_size, input_shape, train_augmentation),
            steps_per_epoch=dataset.train.steps_number(batch_size),
            epochs=train_params.params['epochs'],
            validation_data=dataset.test.prepare_generator(batch_size, input_shape, test_augmentation),
            validation_steps=dataset.test.steps_number(batch_size),
            verbose=1,
            callbacks=[
                *train_params.params.get('callbacks', []),
                ModelCheckpoint(
                    models_ws.path_to('model_epoch{epoch:02d}_loss{val_loss:.3f}.h5'),
                    monitor='val_loss',
                    save_best_only=False),
                ModelCheckpoint(
                    models_ws.path_to('model_epoch{epoch:02d}_best_loss.h5'),
                    monitor='val_loss',
                    verbose=1,
                    save_best_only=True),
                ModelCheckpoint(
                    models_ws.path_to('model_epoch{epoch:02d}_best_accuracy.h5'),
                    monitor='val_acc',
                    verbose=1,
                    save_best_only=True),
                LearningRateLogger(model, target_ws),
                CSVLogger(
                    target_ws.path_to('training_logs.csv'),
                    append=False),
            ])

        return history


class LearningRateLogger(Callback):
    def __init__(self, model, target_ws: Workspace):
        super().__init__()
        self.model = model
        self.target_ws = target_ws

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['lr'] = K.get_value(self.model.optimizer.lr)

    def on_train_end(self, logs=None):
        self.model.to_path(
            self.target_ws.get_ws('output').path_to('model_final.h5'))
