import tkinter as tk
from tkinter import ttk
from typing import Callable, Any

from rx import Observable

EditorProvider = Callable[[tk.Widget, str, str], Any]


class FrameManager(tk.LabelFrame):
    def __init__(self, master: tk.Widget, name: str):
        super().__init__(master, text=name)

        self.notebook = ttk.Notebook(self)
        self.notebook.enable_traversal()
        self.notebook.pack(fill='both', expand='yes')

    def register(self, bus: Observable, editor: EditorProvider):
        bus.pipe(
            # operators.map(select_editor)
        ).subscribe(on_next=lambda event: self.create(event[0], event[1], editor))

    def create(self, name: str, data_path: str, on_create: EditorProvider):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=name, underline=0)
        self.notebook.select(frame)

        item = on_create(frame, name, data_path)
        item.pack(fill='both', expand=True)
