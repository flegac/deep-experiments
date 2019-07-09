import itertools

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

from mydeep_api.dataset.dataset import Dataset


class ConfusionViewer(object):
    def __init__(self, ground_truth: Dataset, predicted: Dataset):
        # Compute confusion matrix
        self.classes = list(set(ground_truth))
        self.cm = confusion_matrix(ground_truth, predicted, labels=self.classes)

    def show(self, normalize: bool = False):
        self._plot(normalize).show()

    def save(self, path: str, normalize: bool = False):
        self._plot(normalize).savefig(path)

    def _plot(self, normalize: bool):
        label = "Normalized" if normalize else "Default"
        title = '{} confusion matrix'.format(label)
        np.set_printoptions(precision=2)
        fig = plt.figure()

        if normalize:
            self.cm = self.cm.astype('float') / self.cm.sum(axis=1)[:, np.newaxis]

        plt.imshow(self.cm, interpolation='nearest', cmap=plt.cm.Blues)
        plt.title(title)
        plt.colorbar()
        tick_marks = np.arange(len(self.classes))
        plt.xticks(tick_marks, self.classes, rotation=45)
        plt.yticks(tick_marks, self.classes)

        fmt = '.2f' if normalize else 'd'
        thresh = self.cm.max() / 2.
        for i, j in itertools.product(range(self.cm.shape[0]), range(self.cm.shape[1])):
            plt.text(j, i, format(self.cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if self.cm[i, j] > thresh else "black")

        plt.ylabel('True label')
        plt.xlabel('Predicted label')
        plt.tight_layout()

        return plt
