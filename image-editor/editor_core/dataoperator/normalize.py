from editor_api.data.data_mixer import Buffer
from editor_api.data.data_operator import DataOperator


class NormalizeOperator(DataOperator):

    def apply(self, source: Buffer) -> Buffer:
        source = source - source.min()
        source = 255 * (source / max(1, source.max()))
        return source.astype('uint8')
