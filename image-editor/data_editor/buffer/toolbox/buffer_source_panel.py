import tkinter as tk
from typing import List

import cv2
from rx.subject import Subject

from data_editor.utils.file_toolbox import FileToolbox
from data_toolbox.buffer.buffer_factory import EmptySource, ImageFactory
from data_toolbox.buffer.operator.normalize import NormalizeOperator
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data.data_operator import DataOperator, PipeOperator
from data_toolbox.data.data_source import DataSource


class BufferSourcePanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='buffer', width=100, height=50)
        self._source = EmptySource()
        self.pipeline: PipeOperator = PipeOperator([NormalizeOperator()])

        self.file_box = FileToolbox(self, lambda _: self.open_image(ImageFactory.from_rgb(_)), self.save_image)
        self.file_box.pack(expand=True, fill='both', side=tk.BOTTOM)

        self.widgets: List[tk.Widget] = []
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)
        self.request_update()

    @property
    def source(self) -> DataSource:
        return self.pipeline.as_source(self._source)

    @property
    def source_descriptor(self):
        buffer = self.source.get_data()
        return '{name} {shape[1]}x{shape[0]} {type}'.format(name=str(self._source),
                                                            shape=buffer.shape,
                                                            type=buffer.dtype)

    def open_image(self, source: BufferSource = None):
        if source is None:
            return
        self._source = source
        self.request_update()

    def save_image(self, path: str = None):
        if path is None or path == '':
            return
        print('save to {}'.format(path))
        img = self.source.get_data()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img)

    def reset(self):
        self.pipeline = PipeOperator()
        self.request_update()

    def push_operator(self, op: DataOperator):
        self.pipeline = self.pipeline | op()
        self.request_update()

    def pop_operator(self):
        self.pipeline = PipeOperator(self.pipeline.pipeline[:-1])
        self.request_update()

    def remove_operator(self, op: DataOperator):
        pipe = self.pipeline.pipeline
        pipe.remove(op)
        self.pipeline = PipeOperator(pipe)
        self.request_update()

    def request_update(self):
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
    widget = BufferSourcePanel(root)
    widget.pack(fill="both", expand=True, side=tk.BOTTOM)

    root.mainloop()
