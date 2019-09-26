import imghdr
import os
import tkinter as tk
from dataclasses import asdict, dataclass, field
from tkinter import ttk
from typing import Callable, Any

from rx.subject import Subject

from data_editor.buffer.image_editor import ImageEditor
from data_editor.table.table_editor import TableEditor
from data_editor.text.text_editor import TextEditor

EditorProvider = Callable[[tk.Widget, str, str], Any]

EDITORS = {
    'dataset': TableEditor,
    'image': ImageEditor,
    'text': TextEditor
}


class EditorNotebook(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str):
        super().__init__(master, text=name)
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=lambda event: self.open_editor(**asdict(event)))

        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.pack(fill='both', expand='yes')
        self.request_update('image', name='editor')

    def open_editor(self, editor_type: str, name: str, path: str):
        if editor_type is not None:
            self._create_editor(name, path, EDITORS[editor_type])
        elif path.endswith('.csv'):
            self._create_editor(name, path, TableEditor)
        elif imghdr.what(path) is not None:
            self._create_editor(name, path, ImageEditor)
        elif path.endswith('.txt') or path.endswith('.json') or path.endswith('.py'):
            self._create_editor(name, path, TextEditor)
        else:
            print('unsupported file format !')

    def _create_editor(self, name: str, data_path: str, on_create: EditorProvider):
        name = name or os.path.basename(data_path)
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name, underline=0)
        self.notebook.select(frame)

        item = on_create(frame, name, data_path)
        item.pack(fill='both', expand=True)

    def request_update(self, editor_type: str = None, name: str = None, path: str = None):
        self.update_bus.on_next(OpenFileEvent(editor_type, name, path))


@dataclass
class OpenFileEvent:
    editor_type: str = field(default=None)
    name: str = field(default=None)
    path: str = field(default=None)


if __name__ == '__main__':
    root = tk.Tk()
    editor = EditorNotebook(root, 'notebook')
    editor.pack()
    root.mainloop()
