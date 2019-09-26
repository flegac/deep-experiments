import tkinter as tk

import cv2
from rx.subject import Subject

from data_editor.project.list_selector_panel import ListSelectorPanel
from data_editor.utils.file_toolbox import FileToolbox
from data_editor.utils.generic_toolbox import GenericToolbox
from data_toolbox.buffer.buffer_factory import EmptySource, ImageFactory
from data_toolbox.buffer.operator.normalize import NormalizeOperator
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data.data_operator import DataOperator, PipeOperator
from data_toolbox.data.data_source import DataSource


class BufferSourcePanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='buffer', width=100, height=50)
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)

        self._source = EmptySource()

        self.text = tk.StringVar()
        label = tk.Label(self, textvariable=self.text)
        label.pack(fill='both', expand=True, side=tk.TOP)

        self.pipeline_panel = ListSelectorPanel(self, 'operators', lambda _: GenericToolbox(_, {
            'Clear': lambda: (_.remove_selected(), self.request_update()),
        }), None)
        self.pipeline_panel.pack(fill="both", expand=True, side=tk.TOP)

        self.pipeline_panel.add_item(NormalizeOperator())

        FileToolbox(self, lambda _: self.open_image(ImageFactory.from_rgb(_)), self.save_image).pack(
            expand=True, fill='both', side=tk.BOTTOM)

        self.request_update()

    @property
    def source(self) -> DataSource:
        pipeline = PipeOperator(self.pipeline_panel.items)
        return pipeline.as_source(self._source)

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
        self.pipeline_panel.remove_all()
        self.request_update()

    def push_operator(self, op: DataOperator):
        self.pipeline_panel.add_item(op())
        self.request_update()

    def request_update(self):
        self.update_bus.on_next(self.source)

    def _redraw(self, event=None):
        self.text.set('{}'.format(self.source_descriptor))


if __name__ == '__main__':
    root = tk.Tk()
    BufferSourcePanel(root).pack(fill="both", expand=True, side=tk.BOTTOM)
    root.mainloop()
