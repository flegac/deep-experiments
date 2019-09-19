from editor.core.data import DataSource, Buffer


class CachedSource(DataSource):
    def __init__(self, delegate: DataSource):
        self.delegate = delegate
        self.data = None

    def invalidate(self):
        self.data = None

    def __call__(self) -> Buffer:
        if self.data is None:
            self.data = self.delegate()
        return self.data