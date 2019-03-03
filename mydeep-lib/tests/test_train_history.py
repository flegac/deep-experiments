from mydeep_lib.dataframe import Dataframes
from mydeep_lib.visualize.train_history import TrainHistory
from surili_core.workspace import Workspace

ws = Workspace.from_path('resources')

df = Dataframes.from_csv(ws.path_to('training_logs.csv'))

hist = TrainHistory(df)

fig = hist.plot_metric('acc')
fig.show()

fig = hist.plot_metric('loss')
fig.show()


