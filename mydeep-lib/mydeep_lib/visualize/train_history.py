import pandas as pd
import matplotlib.pyplot as plt


class TrainHistory(object):
    def __init__(self, history: pd.DataFrame):
        self.history = history

    def plot_metric(self, metric_name):
        dataframe = self.history
        acc = dataframe[metric_name]
        val_acc = dataframe['val_{}'.format(metric_name)]
        epochs = range(1, len(acc) + 1)

        fig = plt.figure()
        plt.title('"{}" history'.format(metric_name))
        plt.plot(epochs, acc, 'red', label='Training')
        plt.plot(epochs, val_acc, 'blue', label='Validation')
        plt.legend()

        return fig
