from keras import backend as K
from keras.callbacks import ModelCheckpoint, CSVLogger, Callback, TensorBoard

from mydeep_api._deprecated.train_dataset import TrainDataset
from mydeep_keras.k_model import KModel
from mydeep_keras.k_train_context import KTrainContext
from surili_core.pipeline_context import PipelineContext
from surili_core.worker import Worker
from surili_core.workspace import Workspace


class KerasTrainer(Worker):
    create_ctx = KTrainContext

    def __init__(self, dataset_path:str,params: KTrainContext) -> None:
        super().__init__()
        self.dataset_path = dataset_path
        self.params = params

    def run(self, ctx: PipelineContext, target_ws: Workspace):
        dataset_ws = target_ws.root.get_ws(self.dataset_path)
        models_ws = target_ws.get_ws('models')

        # load params
        dataset = TrainDataset.from_path(dataset_ws)
        model = self.params.model
        train_params = self.params.params
        train_augmentation = self.params.augmentation.build()
        test_augmentation = self.params.augmentation.build()

        #  save params
        self.save_params(dataset, model, target_ws, train_params)

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
                TensorBoard(
                    log_dir=target_ws.path_to('logs'),
                    histogram_freq=0,
                    batch_size=32,
                    write_graph=True,
                    write_grads=False,
                    write_images=False,
                ),

                CSVLogger(
                    target_ws.path_to('training_logs.csv'),
                    append=False),
            ])

        return history

    def save_params(self, dataset, model, target_ws, train_params):
        params_ws = target_ws.get_ws('params')
        with open(params_ws.path_to('params.json'), 'w') as _:
            _.write(str(train_params))
        with open(params_ws.path_to('augmentation.json'), 'w') as _:
            _.write(str(self.params.augmentation))
        model.to_path(params_ws.path_to('model.h5'))
        dataset.to_path(params_ws.get_ws('dataset'))


class LearningRateLogger(Callback):
    def __init__(self, model: KModel, target_ws: Workspace):
        super().__init__()
        self.k_model = model
        self.target_ws = target_ws

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        logs['lr'] = K.get_value(self.k_model.keras_model.optimizer.lr)

    def on_train_end(self, logs=None):
        self.k_model.to_path(
            self.target_ws.get_ws('output').path_to('model_final.h5'))
