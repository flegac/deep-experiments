import keras

from hyper_search.train_parameters import TrainParameters
from mydeep_keras.k_model import KModel
from mydeep_keras.models.basic_model_v2 import model_v2
from mydeep_lib.worker.prepare_training_dataset import PrepareTrainingDataset
from mydeep_lib.worker.trainer import Trainer
from mydeep_lib.worker.validate_training import ValidateTraining
from sign_mnist.image_file_creation import ImageFileCreation
from sign_mnist.feature_file_creation import FeatureFileCreation
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines_v2.pipelines import pipeline, step

train_ctx = Trainer.create_ctx(

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

pipe = pipeline(
    ctx=ctx,
    steps=[
        step('raw_dataset',
             worker=ImageFileCreation()),
        step('features_dataset',
             worker=FeatureFileCreation(
                 input_path='raw_dataset'
             )),
        step('dataset',
             worker=PrepareTrainingDataset(
                 input_path='features_dataset',
                 test_size=0.1
             )),
        step('training',
             worker=Trainer(train_ctx)),
        step('validation',
             worker=ValidateTraining(train_ctx.augmentation))
    ])
pipe(ctx.project_ws)
