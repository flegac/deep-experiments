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
predictions['y'] = predictions['y'].apply(lambda x: 1 if x > .5 else 0)

cm = ConfusionMatrix(y_expected=expected['y'], y_pred=predictions['y'])
cm.show(classes=[0,1], normalize=True)
