from mydeep_keras.models.basic_model import basic_model
from mydeep_keras.models.basic_model_v2 import model_v2
from mydeep_keras.k_model import KModel


def test_sequential_model():
    model = KModel.from_keras(
        keras_model=basic_model(
            input_shape=(8, 8, 3),
            output_class_number=10,
        ),
        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        })

    model.to_path('model.h5')
    mm = KModel.from_path('model.h5')

    print(mm.keras_model.get_config())


def test_model():
    model = KModel.from_keras(
        keras_model=model_v2(
            input_shape=(8, 8, 3),
            output_class_number=10,
        ),
        compile_params={
            'loss': 'categorical_crossentropy',
            'optimizer': 'Adam',
            'metrics': ['accuracy']
        })

    model.to_path('model2.h5')
    mm = KModel.from_path('model2.h5')

    print(mm.keras_model.get_config())
