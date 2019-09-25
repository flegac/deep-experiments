import tkinter as tk
from typing import List

import cv2
from rx.subject import Subject

from editor_api.data.data_operator import DataOperator, PipelineOperator
from editor_api.data.data_source import DataSource
from editor_api.data.data_utils import EmptySource
from editor_core.datasource.file_source import FileSource
from editor_core.files.gui.file_toolbox import FileToolbox
from editor_core.dataoperator.normalize import NormalizeOperator


class SourceEditor(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='source', width=100, height=50)
        self._source = EmptySource()
        self.pipeline: PipelineOperator = PipelineOperator([NormalizeOperator()])

        self.file_box = FileToolbox(self, self.open_image, self.save_image)
        self.file_box.pack(expand=True, fill='both', side=tk.BOTTOM)

        self.widgets: List[tk.Widget] = []
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)
        self._redraw()

    @property
    def source(self) -> DataSource:
        return self.pipeline.as_source(self._source)

    @property
    def source_descriptor(self):
        buffer = self.source.get_buffer()
        return '{name} {shape[1]}x{shape[0]} {type}'.format(name=str(self._source),
                                                            shape=buffer.shape,
                                                            type=buffer.dtype)

    def open_image(self, path: str = None):
        if path is None or path == '':
            return
        self._source = FileSource.from_rgb(path)
        self.redraw()

    def save_image(self, path: str = None):
        if path is None or path == '':
            return
        print('save to {}'.format(path))
        img = self.source.get_buffer()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img)

    def reset(self):
        self.pipeline = PipelineOperator()
        self.redraw()

    def push_operator(self, op: DataOperator):
        self.pipeline = self.pipeline | op()
        self.redraw()

    def pop_operator(self):
        self.pipeline = PipelineOperator(self.pipeline.pipeline[:-1])
        self.redraw()

    def remove_operator(self, op: DataOperator):
        pipe = self.pipeline.pipeline
        pipe.remove(op)
        self.pipeline = PipelineOperator(pipe)
        self.redraw()

    def redraw(self):
        self.update_bus.on_next(self.source)

    def _redraw(self, source=DataSource):
        for _ in self.widgets:
            _.destroy()

        editor = self

        def _callback(step: DataOperator):
            def run():
                editor.remove_operator(step)

            return run

        self.widgets = [
            tk.Label(self, text=self.source_descriptor),
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
