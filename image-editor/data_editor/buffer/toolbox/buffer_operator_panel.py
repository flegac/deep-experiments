import tkinter as tk

import cv2
from rx.subject import Subject

from data_editor.project.list_selector_panel import ListSelectorPanel
from data_editor.utils.toolbox import Toolbox, FileToolbox
from data_toolbox.buffer.buffer_factory import EmptySource, ImageFactory
from data_toolbox.buffer.operator.normalize import NormalizeOperator
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data.data_operator import DataOperator, PipeOperator
from data_toolbox.data.data_source import DataSource


class BufferOperatorPanel(tk.Frame):
    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master, width=100, height=50)
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)

        self.pipeline_panel = ListSelectorPanel(self, 'operators', lambda _: Toolbox(_, {
            'Clear': lambda: (_.remove_selected(), self.request_update()),
        }), None)
        self.pipeline_panel.pack(fill="both", expand=True, side=tk.TOP)

        self.pipeline_panel.add_item(NormalizeOperator())

        self.request_update()

    @property
    def operator(self) -> DataOperator:
        return PipeOperator(self.pipeline_panel.items)

    def reset(self):
        self.pipeline_panel.remove_all()
        self.request_update()

    def push_operator(self, op: DataOperator):
        self.pipeline_panel.add_item(op())
        self.request_update()

    def request_update(self):
        self.update_bus.on_next(None)

    def _redraw(self, event=None):
        self.pipeline_panel.request_update()


if __name__ == '__main__':
    root = tk.Tk()
    BufferOperatorPanel(root).pack(fill="both", expand=True, side=tk.BOTTOM)
    root.mainloop()
