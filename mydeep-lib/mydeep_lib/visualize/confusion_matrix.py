import itertools

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from sklearn.metrics import confusion_matrix


class ConfusionMatrix(object):
    def __init__(self, y_expected, y_pred):
        # Compute confusion matrix
        self.classes = list(set(y_expected))
        self.cm = confusion_matrix(y_expected, y_pred, labels=self.classes)

    def plot(self, normalize=False) -> Figure:
        label = "Normalized" if normalize else "Default"
        return plot_confusion_matrix(
            self.cm,
            classes=self.classes,
            normalize=normalize,
            title='{} confusion matrix'.format(label))


def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix') -> Figure:
    np.set_printoptions(precision=2)
    fig = plt.figure()

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

    return fig
