import itertools

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix


class ConfusionMatrix(object):
    def __init__(self, y_expected, y_pred):
        # Compute confusion matrix
        self.confusion_matrix = confusion_matrix(y_expected, y_pred, labels = list(y_expected.unique()))
        np.set_printoptions(precision=2)

    def show(self, classes, normalize=False):
        label = "Normalized" if normalize else "Default"
        plot_confusion_matrix(self.confusion_matrix, classes=classes, normalize=normalize,
                              title='{} confusion matrix'.format(label))


def plot_confusion_matrix(confusion_matrix, classes,
                          normalize=False,
                          title='Confusion matrix'):
    fig = plt.figure()

    if normalize:
        confusion_matrix = confusion_matrix.astype('float') / confusion_matrix.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')
    print(confusion_matrix)

    plt.imshow(confusion_matrix, interpolation='nearest', cmap=plt.cm.Blues)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = confusion_matrix.max() / 2.
    for i, j in itertools.product(range(confusion_matrix.shape[0]), range(confusion_matrix.shape[1])):
        plt.text(j, i, format(confusion_matrix[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if confusion_matrix[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

    plt.show()
