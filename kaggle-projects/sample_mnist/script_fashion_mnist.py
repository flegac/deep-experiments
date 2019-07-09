import keras

from hyper_search.train_parameters import TrainParameters
from mydeep_keras.models.basic_model import basic_model
from mydeep_keras.keras_model import KModel
from mydeep_train.prepare_training_dataset import PrepareTrainingDataset
from mydeep_train.trainer import Trainer
from mydeep_train.validate_training import ValidateTraining
from sample_mnist.prepare_mnist import PrepareMnist
from surili_core.pipelines import pipeline
from surili_core.pipeline_context import PipelineContext

train_ctx = Trainer.create_ctx(

    model_provider=lambda: KModel.from_keras(
        basic_model(
            input_shape=(28, 28, 1),
            output_class_number=10,
        ),
        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 2048,
        'epochs': 10,
        'callbacks': [
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                mode='auto',
                factor=0.5,
                patience=2,
                cooldown=0,
                min_delta=1e-4,
                min_lr=1e-9,
            ),
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                mode='auto',
                min_delta=0,
                patience=10,
                verbose=0,
                baseline=None,
                restore_best_weights=False
            )
        ]
    }),
    augmentation=TrainParameters({
        '__builder__': keras.preprocessing.image.ImageDataGenerator,
        'rotation_range': 10,
        'width_shift_range': 0.1,
        'height_shift_range': 0.1,
        'shear_range': 0.3,
        'zoom_range': 0.1,
    })
)

pipe = pipeline([
    PrepareMnist(),
    PrepareTrainingDataset(test_size=0.1),
    Trainer(train_ctx),
    ValidateTraining(train_ctx.augmentation)
])

pipe(PipelineContext(
    root_path='D:/Datasets/fashion_mnist',
    project_name='fashion_mnist'))
