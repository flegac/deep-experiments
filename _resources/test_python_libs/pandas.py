import pandas as pd
import numpy as np
import matplotlib.pylab as plt

df = pd.read_csv('../../kaggle_mnist/resources/input/test.csv')

head = df.head(3)
head = np.array(head)

print(head.shape)
print(head)

head = np.reshape(head, (head.shape[0], 28, 28))


def _plot_measure(data):
    x_axis = range(data.shape[0])
    plt.figure()
    plt.title('my title')
    plt.plot(x_axis, data, label='Training')
    plt.legend()
    plt.show()


N = 10
K = 2
data = np.random.rand(N, K)

_plot_measure(data)

_plot_measure(head)
