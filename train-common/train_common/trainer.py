from keras.callbacks import ModelCheckpoint, CSVLogger, LambdaCallback
from keras.preprocessing.image import ImageDataGenerator

from surili_core.pipeline_worker import PipelineWorker
from surili_core.workspace import Workspace
from train_common.ctx.dataset import TrainingDataset, Dataset
from train_common.ctx.train_context import TrainContext


class Trainer(PipelineWorker):
    def __init__(self, params: TrainContext) -> None:
        super().__init__('model training', 'training')
        self.params = params
        self.x = 'x'
        self.y = 'y'

    def apply(self, target_ws: Workspace):
        dataset_ws = self.ctx.project_ws.get_ws('dataset')
        models_ws = target_ws.get_ws('models')
        params_ws = target_ws.get_ws('params')

        # load params
        dataset = TrainingDataset.from_path(dataset_ws)
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

        batch_size = train_params.params['batch_size']

        def prepare_generator(data: Dataset, augmentation: ImageDataGenerator):
            df = data.df

            image_path = '{}.' + data.img_ext
            df[self.x] = df[self.x].map(image_path.format)
            return augmentation.flow_from_dataframe(
                df,
                x_col=self.x, y_col=self.y,
                classes=list(df[self.y].unique()),
                directory=data.img_path,
                target_size=model.input_shape(),
                batch_size=batch_size,
                class_mode='categorical'
            )

        # ----- cancer_detection -------------------------------------------------------------
        train = prepare_generator(dataset.train, train_augmentation)
        history = model.keras_model.fit_generator(
            train,
            steps_per_epoch=dataset.train.steps_number(batch_size),
            epochs=train_params.params['epochs'],
            validation_data=prepare_generator(dataset.test, test_augmentation),
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
                CSVLogger(
                    target_ws.path_to('training_logs.csv'),
                    append=False),
                LambdaCallback(
                    on_train_end=lambda logs: model.to_path(
                        target_ws.get_ws('output').path_to('model_final.h5'))),
            ])
        return history
