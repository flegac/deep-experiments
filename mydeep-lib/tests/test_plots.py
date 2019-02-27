import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# history
dataset = pd.read_csv('D:\Datasets\histopathologic-cancer-detection\_workspaces\_workspace_1\\dataset\\dataset.csv')
history = pd.read_csv(
    'D:\Datasets\histopathologic-cancer-detection\_workspaces\\training_logs.csv')


# df.plot.scatter(x='epoch', y='val_acc').get_figure().show()
# history.plot.hexbin(x='epoch', y='val_acc', gridsize=30).get_figure().show()


def plot_history(history, dataset):
    fig, axarr = plt.subplots(nrows=2, ncols=2, figsize=(12, 12))
    history.plot.line(x='epoch', y=['acc', 'val_acc'], ax=axarr[1][0])
    history.plot.line(x='epoch', y=['loss', 'val_loss'], ax=axarr[1][1])

    # category repartition
    dataset = dataset.loc[:, ['id', 'label']]
    dataset['label'].value_counts().plot.bar(ax=axarr[0][0])

    fig.show()


plot_history(history, dataset)

# prediction repartition
df_v1 = pd.read_csv(
    'D:\Datasets\histopathologic-cancer-detection\_workspaces\_workspace\\final_predictions.csv')


def show_reparition(df):
    # df['label'].value_counts(normalize=True, sort=True).plot.bar().get_figure().show()
    factors = pd.cut(df['label'], [0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1])
    print(pd.value_counts(factors))
