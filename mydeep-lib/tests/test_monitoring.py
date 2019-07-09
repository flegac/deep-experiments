import pandas as pd

from mydeep_api.data import Data
from mydeep_api.monitoring.confusion_viewer import ConfusionViewer
from mydeep_api.monitoring.dataset_viewer import DatasetViewer
from mydeep_api.monitoring.history_viewer import HistoryViewer
from surili_core.workspace import Workspace

ws = Workspace.from_path('resources')


def test_history_monitoring():
    hist = HistoryViewer.from_path(ws.path_to('training_logs.csv'))

    hist.show('loss', 'acc')


def test_dataset_monitoring():
    db = Data.from_folder_tree(x_path=ws.path_to('dataset/folder_tree'))
    DatasetViewer(
        dataset=db.x,
        label='dataset',
        scale=2
    ).show(n=None)


def test_confusion_viewer():
    expected = pd.DataFrame({
        'x': [0, 1, 2, 3],
        'y': [0, 0, 1, 1],

    })

    predictions = pd.DataFrame({
        'x': [0, 1, 2, 3],
        'y': [.1, .5, 1, .3],
    })
    pred = (predictions['y'] > .5).astype(int)

    cm = ConfusionViewer(ground_truth=expected['y'], predicted=pred)
    cm.show(normalize=True)
