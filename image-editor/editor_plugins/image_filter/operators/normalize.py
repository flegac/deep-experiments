from editor_api.data import DataOperator, Buffer


class NormalizeOperator(DataOperator):

    def apply(self, data: Buffer) -> Buffer:
        data = data - data.min()
        data = 255 * (data / max(1, data.max()))
        return data.astype('uint8')


