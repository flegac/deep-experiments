from typing import Tuple

from keras.engine import Layer
from keras.layers import Conv2D, BatchNormalization, Activation

from mydeep_keras.models.blocks.block import Block


class Conv(Block):

    def __init__(self,
                 filters: int,
                 kernel_size: Tuple[int, int] = (3, 3),
                 strides: Tuple[int, int] = (1, 1),
                 activation: str = 'relu',
                 padding='same'):

        self.padding = padding
        self.activation = activation
        self.strides = strides
        self.kernel_size = kernel_size
        self.filters = filters

    def build(self, x: Layer):
        if self.kernel_size != (1, 1):
            x = Conv2D(filters=self.filters,
                       kernel_size=(self.kernel_size[0], 1),
                       strides=(self.strides[0], 1),
                       padding=self.padding, )(x)
            x = BatchNormalization()(x)
            x = Activation(self.activation)(x)
            x = Conv2D(filters=self.filters,
                       kernel_size=(1, self.kernel_size[1]),
                       strides=(1, self.strides[1]),
                       padding=self.padding, )(x)
            x = BatchNormalization()(x)
            x = Activation(self.activation)(x)
        else:
            x = Conv2D(filters=self.filters,
                       kernel_size=self.kernel_size,
                       strides=self.strides,
                       padding=self.padding, )(x)
            x = BatchNormalization()(x)
            x = Activation(self.activation)(x)
        return x
