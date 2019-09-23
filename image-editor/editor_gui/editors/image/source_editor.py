import tkinter as tk
from typing import List

import cv2
from rx.subject import Subject

from editor_api.data.data_core import DataOperator, DataSource, PipelineOperator
from editor_api.data.data_utils import EmptySource
from editor_core.file_source import FileSource
from editor_plugins.image_filter.operators.normalize import NormalizeOperator


class SourceEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='source', width=100, height=50)
        self._source = EmptySource()
        self.pipeline: PipelineOperator = PipelineOperator([NormalizeOperator()])

        self.widgets: List[tk.Widget] = []
        self.source_change_bus = Subject()
        self.source_change_bus.subscribe(on_next=self.redraw_pipeline)
        self.redraw_pipeline()

    def open_image(self, path: str = None):
        if path is None or path == '':
            return
        self._source = FileSource.from_rgb(path)
        self._post_new_source()

    def save_image(self, path: str = None):
        if path is None or path == '':
            return
        print('save to {}'.format(path))
        img = self.get_source().get_buffer()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img)

    def reset(self):
        self.pipeline = PipelineOperator()
        self._post_new_source()

    def push_operator(self, op: DataOperator):
        self.pipeline = self.pipeline | op()
        self._post_new_source()

    def pop_operator(self):
        self.pipeline = PipelineOperator(self.pipeline.pipeline[:-1])
        self._post_new_source()

    def remove_operator(self, op: DataOperator):
        pipe = self.pipeline.pipeline
        pipe.remove(op)
        self.pipeline = PipelineOperator(pipe)
        self._post_new_source()

    def get_source(self) -> DataSource:
        return self._source | self.pipeline

    def _post_new_source(self):
        self.source_change_bus.on_next(self.get_source())

    def redraw_pipeline(self, source=DataSource):
        for _ in self.widgets:
            _.destroy()

        editor = self

        def _callback(step: DataOperator):
            def run():
                editor.remove_operator(step)

            return run

        self.widgets = [
            tk.Label(self, text=str(self._source)),
            *[
                tk.Button(self, text=str(step), command=_callback(step))
                for step in self.pipeline.pipeline
            ]
        ]
        if len(self.widgets) > 1:
            self.widgets.append(tk.Button(self, text='Reset', command=self.reset))

        for _ in self.widgets:
            _.pack(fill="both", expand=True, side=tk.TOP)


if __name__ == '__main__':
    root = tk.Tk()
    widget = SourceEditor(root)
    widget.pack(fill="both", expand=True, side=tk.BOTTOM)

    root.mainloop()
