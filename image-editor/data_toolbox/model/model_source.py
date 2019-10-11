from data_toolbox.data.data_source import DataSource
from data_toolbox.model.model import Model


class ModelSource(DataSource[Model]):
    def __init__(self, model: Model):
        self._source = model

    def get_data(self) -> Model:
        return self.get_model()

    def get_model(self) -> Model:
        return self._source

    def __repr__(self):
        return 'Model[{}]'.format(self._source)
