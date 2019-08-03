import abc

from keras.engine import Layer


class Block(abc.ABC):
    def __call__(self, x: Layer) -> Layer:
        return self.build(x)

    def build(self, x: Layer) -> Layer:
        raise NotImplementedError()
