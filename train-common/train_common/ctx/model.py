import json

import keras


class Model(object):
    # TODO: test if model.get_config() save the compilation options (optimizer, loss ...) in its json representation

    # TODO : robustify serialization - use keras.models.load_model / keras_model.save()

    @staticmethod
    def from_keras(keras_model: keras.Model, compile_params: dict):
        if compile_params:
            keras_model.compile(**compile_params)
        return Model(keras_model)

    @staticmethod
    def from_path(path: str):
        assert path.endswith('.h5')
        config_path = path.replace('.h5', '.json')

        try:
            with open(config_path) as _:
                keras_model = keras.Sequential.from_config(json.load(_))
        except:
            with open(config_path) as _:
                keras_model = keras.Model.from_config(json.load(_))
        keras_model.load_weights(path)
        return Model(keras_model)

    def __init__(self, keras_model: keras.Model):
        self.keras_model = keras_model

    def input_shape(self):
        return self.keras_model.get_layer(index=0).input_shape[1:-1]

    def output_shape(self):
        return self.keras_model.get_layer(index=-1).output_shape[1:]

    def to_path(self, path: str):
        assert path.endswith('.h5')

        config_path = path.replace('.h5', '.json')

        with open(path.replace('.h5', '_summary.txt'), 'w') as _:
            self.keras_model.summary(print_fn=lambda x: _.write(str(x) + '\n'))

        with open(config_path, 'w') as _:
            json.dump(self.keras_model.get_config(), _, indent=2)
        self.keras_model.save_weights(path)
