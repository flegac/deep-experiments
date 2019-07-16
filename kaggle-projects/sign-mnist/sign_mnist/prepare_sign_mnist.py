import pandas as pd


def name_provider(df: pd.DataFrame):
    def compute_name(index):
        label = df['y'][index]
        return 'cat{}_id{}'.format(label, index)

    return compute_name
