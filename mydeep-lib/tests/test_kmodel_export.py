from mydeep_keras.k_model import KModel
from mydeep_keras.models.basic_model_v2 import model_v2
from surili_core.workspace import Workspace

ws = Workspace.from_path('resources/model')


def test_model_export():
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

    model_path = ws.path_to('model2.h5')
    model.to_path(model_path)
    mm = KModel.from_path(model_path)

    print(mm.keras_model.get_config())
