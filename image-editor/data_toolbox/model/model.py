import keras
from efficientnet.keras import EfficientNetB0


class Model(object):

    @staticmethod
    def from_scratch():
        model = EfficientNetB0(weights='imagenet')
        return Model(model)

    @staticmethod
    def from_h5(path: str):
        model = keras.models.load_model(path)
        return Model(model)

    def __init__(self, keras_model):
        self.keras_model = keras_model

    def __repr__(self):
        return str(self.keras_model)
