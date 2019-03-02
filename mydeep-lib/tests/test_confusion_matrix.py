import pandas as pd

from mydeep_lib.visualize.confusion_matrix import ConfusionMatrix

expected = pd.DataFrame({
    'x': [0, 1, 2, 3],
    'y': [0, 0, 1, 1],

})

predictions = pd.DataFrame({
    'x': [0, 1, 2, 3],
    'y': [.1, .5, 1, .3],
})
pred = (predictions['y'] > .5).astype(int)

cm = ConfusionMatrix(y_expected=expected['y'], y_pred=pred)
fig = cm.plot(normalize=True)
fig.show()
# fig.savefig('output.png')
