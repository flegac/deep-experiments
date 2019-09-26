import tkinter as tk
from typing import List, Dict, Callable, Any, Set

from rx.subject import Subject

from data_editor.utils.generic_toolbox import GenericToolbox
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data.data_source import DataSource


class ListSelectorPanel(tk.Frame):
    def __init__(self, master: tk.Widget,
                 name: str,
                 toolbox_provider: 'Callable[[ListSelectorPanel], GenericToolbox]',
                 on_open: Callable[[BufferSource], Any] = None):
        tk.Frame.__init__(self, master)
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)

        self._items: Set[DataSource] = set()

        self.name = name

        # action box
        toolbox_provider(self).pack(expand=True, fill='both', side=tk.BOTTOM)

        self._widgets: List[tk.Widget] = []
        self._checkboxes: Dict[DataSource, tk.IntVar] = dict()

        self.on_open = on_open
        self.request_update()

    def add_item(self, item: Any):
        if item is None:
            return
        self._items.add(item)
        self.request_update()

    @property
    def items(self):
        return self._items

    def get_selection(self):
        selected = []
        for item, var in self._checkboxes.items():
            if var.get() > 0:
                selected.append(item)
        return selected

    def remove_selected(self):
        selected = self.get_selection()
        for _ in selected:
            self._items.remove(_)
        if len(selected) > 0:
            self.request_update()

    def request_update(self):
        self.update_bus.on_next(None)

    def _redraw(self, event=None):
        for _ in self._widgets:
            _.destroy()
        self._widgets.clear()
        self._checkboxes.clear()

        self._create_group(self.name, self._items)

    def _create_group(self, label: str, sources: List[DataSource]):
        frame = tk.LabelFrame(self, text=label, width=100, height=25)
        frame.pack(fill="both", expand=True, side=tk.TOP)
        for source in sources:
            widget, var = self._create_row_widget(frame, source)
            self._checkboxes[source] = var
        self._widgets.append(frame)

    def _create_row_widget(self, parent: tk.Frame, item: Any):
        var = tk.IntVar()

        def open_callback(source: BufferSource):
            def run():
                print('open : {}'.format(source))
                self.on_open(source)

            return run

        widget = tk.Frame(parent)
        tk.Checkbutton(widget, command=lambda: None, variable=var).pack(fill="both", expand=False, side=tk.LEFT)
        tk.Button(widget, text=str(item), command=open_callback(item)).pack(fill="both", expand=True, side=tk.RIGHT)
        widget.pack(fill="both", expand=True, side=tk.TOP)
        return widget, var

    def remove_all(self):
        self._items.clear()
        self.request_update()


if __name__ == '__main__':
    root = tk.Tk()
    ListSelectorPanel(root, 'selector', lambda _: GenericToolbox(_, {
        'test1': lambda: None,
        'test2': lambda: None
    }), None).pack(fill="both", expand=True, side=tk.BOTTOM)
    root.mainloop()
