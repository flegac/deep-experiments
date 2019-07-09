import pandas as pd

from mydeep_api.monitoring.confusion_viewer import ConfusionViewer

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
fig = cm.plot(normalize=True)
fig.show()
# fig.savefig('output.png')
