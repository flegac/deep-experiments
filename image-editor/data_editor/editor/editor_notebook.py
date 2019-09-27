import imghdr
import tkinter as tk
from tkinter import ttk
from typing import Callable, Any

from dataclasses import dataclass, field
from rx.subject import Subject

from data_editor.buffer.image_editor import ImageEditor
from data_editor.table.table_view import TableView
from data_editor.text.text_view import TextView
from data_toolbox.buffer.buffer_factory import ImageFactory
from data_toolbox.buffer.source.buffer_source import BufferSource
from data_toolbox.data.data_source import DataSource
from data_toolbox.table.table_source import TableSource

EditorProvider = Callable[[tk.Widget, str, str], Any]

EDITORS = {
    'dataset': TableView,
    'image': ImageEditor
}


class EditorNotebook(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str):
        super().__init__(master, text=name)
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=lambda event: self.open_editor(event.source))

        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.pack(fill='both', expand='yes')
        self.request_update(ImageFactory.empty)

    def open_editor(self, source: DataSource):
        name = str(source)
        if isinstance(source, BufferSource):
            factory = ImageEditor
        elif isinstance(source, TableSource):
            factory = TableView
        elif isinstance(source, str):
            # TODO: create TextSource --> source is a path to a file here :(
            factory = TextView
        else:
            raise ValueError('unsupported file format !')

        selected = self.notebook.select()
        if selected != '':
            self.notebook.forget(selected)

        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name, underline=0)
        self.notebook.select(frame)

        item = factory(frame, name, source)
        item.pack(fill='both', expand=True)

    def request_update(self, source: DataSource):
        if isinstance(source, str):
            path = source
            if path.endswith('.csv'):
                source = TableSource().load(path)
            elif imghdr.what(path) is not None:
                source = ImageFactory.from_rgb(path)
            elif path.endswith('.txt') or path.endswith('.json') or path.endswith('.py'):
                # TODO create TextSource
                pass
            else:
                print('unsupported file format !')
        self.update_bus.on_next(OpenSourceEvent(source))


@dataclass
class OpenSourceEvent:
    source: DataSource = field(default=None)


if __name__ == '__main__':
    root = tk.Tk()
    EditorNotebook(root, 'notebook').pack()
    root.mainloop()
