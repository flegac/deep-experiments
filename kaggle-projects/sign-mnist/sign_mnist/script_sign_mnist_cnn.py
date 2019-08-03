import keras

from hyper_search.train_parameters import TrainParameters
from mydeep_keras.k_model import KModel
from mydeep_keras.k_trainer import KerasTrainer
from mydeep_keras.models.basic_model_v2 import model_v2
from mydeep_workers.prepare_training_dataset import PrepareTrainingDataset
from mydeep_workers.validate_training import ValidateTraining
from sign_mnist.feature_dataset_creation import FeatureDatasetCreation
from sign_mnist.raw_dataset_creation import RawDatasetCreation
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline, step

train_ctx = KerasTrainer.create_ctx(

    model_provider=lambda: KModel.from_keras(

        # keras_model(
        #     input_shape=(32, 32, 3),
        #     output_class_number=24,
        #     weights=None,
        #     k_model=keras.applications.mobilenet_v2.MobileNetV2,
        #     alpha=1
        # ),

        # basic_model(
        #     input_shape=(28, 28, 3),
        #     output_class_number=24,
        # ),

        model_v2(
            input_shape=(28, 28, 3),
            output_class_number=24,
        ),

        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 64,
        'epochs': 1,
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
    root_path='D:/Datasets/sign-language-mnist',
    project_name='sign-mnist-cnn'
)

pipeline([
    step('raw_dataset',
         worker=RawDatasetCreation()),
    step('features_dataset',
         worker=FeatureDatasetCreation(
             input_path='raw_dataset'
         )),
    step('dataset',
         worker=PrepareTrainingDataset(
             input_path='features_dataset',
             test_size=0.1
         )),
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
         )),
])(ctx)
