import cv2
import keras
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

from data_toolbox.data.data_operator import DataOperator
from data_toolbox.image.buffer import Buffer
from data_toolbox.model.model_source import ModelSource


class ModelViewer(DataOperator):
    def __init__(self, source: ModelSource, target_path:str):
        model = source.get_model().keras_model
        inputs = model.input
        outputs = [_ for _ in model.layers if isinstance(_, keras.layers.Activation)]
        self.model = keras.models.Model(inputs=inputs, outputs=[_.output for _ in outputs])
        self.layer_names = [_.name for _ in outputs]
        self.model.summary()

        self.target_path=target_path

    def apply(self, source: Buffer) -> Buffer:
        data = cv2.resize(source, tuple(self.model.input.shape[1:3]))
        data = np.expand_dims(data, 0)

        activations = self.model.predict(data)

        images_per_row = 16

        fig = plt.figure()
        for i, (layer_name, layer_activation) in enumerate(zip(self.layer_names, activations)):
            _, w, h, n_features = layer_activation.shape
            n_cols = n_features // images_per_row
            display_grid = np.zeros((w * n_cols, images_per_row * h))
            for col in range(n_cols):
                for row in range(images_per_row):
                    channel = layer_activation[0, :, :, col * images_per_row + row]
                    channel -= channel.mean()
                    channel /= channel.std()
                    channel *= 64
                    channel += 128
                    channel = np.clip(channel, 0, 255).astype('uint8')
                    display_grid[col * w: (col + 1) * w, row * h: (row + 1) * h] = channel
            # plt.figure(figsize=(display_grid.shape[1] / w, display_grid.shape[0] / h))
            # plt.title(layer_name)
            # plt.grid(False)
            # plt.imshow(display_grid, aspect='auto', cmap='viridis')
            ax = fig.add_subplot(len(activations), 1, i + 1)
            ax.matshow(display_grid, cmap='binary')
            ax.axis('off')
            ax.margins(0.01)
            plt.xticks(np.array([]))
            plt.yticks(np.array([]))

        fig.tight_layout()
        plt.savefig(self.target_path, dpi=100)

        return source

    def show(self):
        plt.close('all')

        layers = self.model.layers
        for _ in layers:
            if isinstance(_, keras.layers.Conv2D):
                weights = _.weights[0]
                plot_filters(weights)


def plot_multi_bands(data: Buffer):
    w, h, b = data.shape

    n = int(np.ceil(np.sqrt(b)))

    fig = plt.figure()
    for i in range(b):
        ax = fig.add_subplot(1, 1, 1)
        ax.matshow(data, cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))

    fig.tight_layout()
    fig.show()


def plot_filters(weights: Buffer):
    w, h, n1, n2 = weights.shape
    try:
        data = weights.numpy()
    except:
        data = weights
    data = np.moveaxis(data, (0, 1), (1, 3))
    data = data.reshape((w * n1, h * n2))
    # data = scipy.ndimage.zoom(data, (20, 20))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.matshow(data, cmap=matplotlib.cm.binary)
    plt.xticks(np.array([]))
    plt.yticks(np.array([]))

    fig.tight_layout()
    fig.show()
