from data_toolbox.data.data_mixer import Buffer
from data_toolbox.data.data_operator import DataOperator


class NormalizeOperator(DataOperator):

    def apply(self, source: Buffer) -> Buffer:
        source = source - source.min()
        source = 255 * (source / max(1, source.max()))
        return source.astype('uint8')
