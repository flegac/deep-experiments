from keras.engine import Layer
from keras.layers import Concatenate, GlobalMaxPooling2D, GlobalAveragePooling2D, Flatten, Dropout, Dense, Activation

from mydeep_keras.models.blocks.block import Block


class Output(Block):
    def __init__(self,
                 class_number: int,
                 activation: str = 'sigmoid',
                 dropout: float = .5):
        self.class_number = class_number
        self.activation = activation
        self.dropout = dropout

    def build(self, x: Layer):
        x = Concatenate(axis=-1)([
            GlobalMaxPooling2D()(x),
            GlobalAveragePooling2D()(x),
            Flatten()(x)
        ])
        x = Dropout(self.dropout)(x)
        x = Dense(self.class_number)(x)
        x = Activation(self.activation)(x)
        return x
