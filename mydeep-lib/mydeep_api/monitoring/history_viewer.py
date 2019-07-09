from typing import List

import matplotlib.pyplot as plt
import pandas as pd


class HistoryViewer(object):
    @staticmethod
    def from_path(path: str):
        assert path.endswith('.csv')
        return HistoryViewer(pd.read_csv(path))

    @staticmethod
    def from_dataframe(history: pd.DataFrame):
        return HistoryViewer(history)

    def __init__(self, history: pd.DataFrame):
        self.history = history
        self.scale = 1

    def show(self, *metric_names: List[str]):
        self._plot(*metric_names).show()

    def save(self, path: str, *metric_names: List[str]):
        self._plot(*metric_names).savefig(path)

    def _plot(self, *metric_names: List[str]):
        dataframe = self.history

        lines = len(metric_names)
        fig, ax = plt.subplots(nrows=lines)
        ax = ax.reshape(lines)
        ax[0].set_title('{}'.format(metric_names), size='large')

        for i, metric_name in enumerate(metric_names):
            acc = dataframe[metric_name]
            val_acc = dataframe['val_{}'.format(metric_name)]
            epochs = range(1, len(acc) + 1)
            ax[i].plot(epochs, acc, 'red', label='Training {}'.format(metric_name))
            ax[i].plot(epochs, val_acc, 'blue', label='Validation {}'.format(metric_names))
            ax[i].legend()

        return plt
