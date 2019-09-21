import imghdr
import os
import tkinter as tk
from dataclasses import asdict
from tkinter import ttk
from typing import Callable, Any

from editor_gui.editors.dataset_editor import DatasetEditor
from editor_gui.editors.image.image_editor import ImageEditor
from editor_gui.editors.text_editor import TextEditor
from editor_gui.event_bus import FILE_OPEN_BUS, OpenFileEvent

EditorProvider = Callable[[tk.Widget, str, str], Any]

EDITORS = {
    'dataset': DatasetEditor,
    'image': ImageEditor,
    'text': TextEditor
}


class EditorNotebook(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str):
        super().__init__(master, text=name)
        FILE_OPEN_BUS.subscribe(on_next=lambda event: self.open_editor(**asdict(event)))

        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.pack(fill='both', expand='yes')
        FILE_OPEN_BUS.on_next(OpenFileEvent('image', name='editor'))

    def open_editor(self, editor_type: str, name: str, path: str):
        if editor_type is not None:
            self._create_editor(name, path, EDITORS[editor_type])
        elif path.endswith('.csv'):
            self._create_editor(name, path, DatasetEditor)
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
