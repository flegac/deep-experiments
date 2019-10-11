import tkinter as tk
from typing import Callable, Any

from rx.subject import Subject

from data_editor.utils.list_selector_panel import ListSelectorPanel
from data_editor.utils.toolbox import Toolbox
from data_toolbox.image.op.normalize import NormalizeOperator
from data_toolbox.data.data_operator import DataOperator, PipeOperator


class OperatorPanel(tk.Frame):
    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master, width=100, height=50)
        self._observer = Subject()

        self.pipeline_panel = ListSelectorPanel(self, 'operators', lambda _: Toolbox(_, {
            'Clear': lambda: (_.remove_selected(),self._observer.on_next(None)),
        }), None)
        self.pipeline_panel.pack(fill="both", expand=True, side=tk.TOP)
        self.push_operator(NormalizeOperator)

    def subscribe(self, on_next: Callable[[Any], None]):
        return self._observer.subscribe(on_next=on_next)

    @property
    def operator(self) -> DataOperator:
        return PipeOperator(self.pipeline_panel.items)

    def reset(self):
        self.pipeline_panel.remove_all()
        self._observer.on_next(None)

    def push_operator(self, op: type(DataOperator)):
        self.pipeline_panel.add_item(op())
        self._observer.on_next(None)


if __name__ == '__main__':
    root = tk.Tk()
    OperatorPanel(root).pack(fill="both", expand=True, side=tk.BOTTOM)
    root.mainloop()
