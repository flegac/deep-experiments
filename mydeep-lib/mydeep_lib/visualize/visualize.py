from mydeep_lib.visualize.show_dataset import ShowDataset
import matplotlib.pyplot as plt
import pandas as pd


class Visualize:
    @staticmethod
    def show_dataset(label='Dataset', scale=5):
        return ShowDataset(label, scale)

    @staticmethod
    def show_plot(plot):
        plot.show()

    @staticmethod
    def save_plot(path):
        def apply(plot):
            plot.savefig('{}.pdf'.format(path))
            plot.savefig('{}.png'.format(path))

        return apply

    @staticmethod
    def history_from_dataframe(dataframe):
        acc = dataframe['categorical_accuracy']
        val_acc = dataframe['val_categorical_accuracy']
        loss = dataframe['loss']
        val_loss = dataframe['val_loss']
        epochs = range(1, len(acc) + 1)

        fig = plt.figure()
        plt.title('Training and validation loss and accuracy')
        plt.plot(epochs, acc, 'red', label='Training acc')
        plt.plot(epochs, val_acc, 'blue', label='Validation acc')
        plt.legend()

        plt.plot(epochs, loss, 'cyan', label='Training loss')
        plt.plot(epochs, val_loss, 'green', label='Validation loss')
        plt.legend()
        return fig

    @staticmethod
    def history_from_path(path: str):
        return Visualize.history_from_dataframe(pd.read_csv(path))
