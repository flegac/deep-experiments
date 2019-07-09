import keras

from hyper_search.train_parameters import TrainParameters
from monkeys_detection.prepare_monkeys import PrepareMonkeys
from mydeep_lib.models.basic_model import basic_model
from mydeep_train.compute_submission import ComputeSubmission
from mydeep_api.model.keras_model import KModel
from mydeep_train.prepare_training_dataset import PrepareTrainingDataset
from mydeep_train.validate_training import ValidateTraining
from surili_core.pipeline_context import PipelineContext
from surili_core.pipelines import pipeline
from mydeep_train.search_learning_rate import SearchLearningRate
from mydeep_train.trainer import Trainer

train_ctx = Trainer.create_ctx(

    model_provider=lambda: KModel.from_keras(
        basic_model(
            input_shape=(128, 128, 3),
            output_class_number=10,
        ),
        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'SGD',
            'metrics': ['accuracy']
        }),

    params=TrainParameters({
        'batch_size': 64,
        'epochs': 2,
        'callbacks': [
            # CyclicLR(
            #     base_lr=1e-6,
            #     max_lr=1e-2,
            #     step_size=5,
            #     mode='triangular'
            # ),
            # SGDRScheduler(
            #     min_lr=1.e-5,
            #     max_lr=1.e-2,
            #     steps_per_epoch=np.ceil(137 / 137),
            #     lr_decay=.9,
            #     cycle_length=5,
            # )
            # keras.callbacks.ReduceLROnPlateau(
            #     monitor='val_loss',
            #     mode='auto',
            #     factor=0.5,
            #     patience=2,
            #     cooldown=0,
            #     min_delta=1e-4,
            #     min_lr=1e-9,
            # ),
            # keras.callbacks.EarlyStopping(
            #     monitor='val_loss',
            #     mode='auto',
            #     min_delta=0,
            #     patience=10,
            #     verbose=0,
            #     baseline=None,
            #     restore_best_weights=False
            # )
        ]
    }),

    augmentation=TrainParameters({
        '__builder__': keras.preprocessing.image.ImageDataGenerator,
        'rescale': 1. / 255,
        'rotation_range': 40,
        'width_shift_range': 0.2,
        'height_shift_range': 0.2,
        'shear_range': 0.2,
        'zoom_range': 0.2,
        'horizontal_flip': True,
    })
)

pipe = pipeline([
    PrepareMonkeys(),
    PrepareTrainingDataset(test_size=0.1),
    SearchLearningRate(train_ctx, min_lr=0.69, max_lr=0.71),
    Trainer(train_ctx),
    ValidateTraining(train_ctx.augmentation),
    ComputeSubmission(train_ctx.augmentation, nb_pred=2, target_x='xx', target_y='yy')
])
pipe(PipelineContext(
    root_path='D:/Datasets/10-monkey-species',
    project_name='monkeys'))
