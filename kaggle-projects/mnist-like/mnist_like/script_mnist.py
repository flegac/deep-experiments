import keras

from hyper_search.train_parameters import TrainParameters
from mnist_like.prepare_mnist import PrepareMnist
from mydeep_keras.k_model import KModel
from mydeep_keras.k_trainer import KerasTrainer
from mydeep_keras.models.basic_model import basic_model
from mydeep_workers.prepare_training_dataset import PrepareTrainingDataset
from mydeep_workers.validate_training import ValidateTraining
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline, step

train_ctx = KerasTrainer.create_ctx(

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

ctx = PipelineContext(
    root_path='D:/Datasets/mnist',
    project_name='mnist'
)

pipe = pipeline([
    step('raw_dataset',
         worker=PrepareMnist()),
    step('dataset',
         worker=PrepareTrainingDataset(input_path='raw_dataset', test_size=0.1)),
    step('training',
         worker=KerasTrainer(
             dataset_path='dataset',
             params=train_ctx
         )),
    step('validation',
         worker=ValidateTraining(
             training_path='training',
             dataset_path='dataset',
             augmentation=train_ctx.augmentation
         ))
])(ctx)
