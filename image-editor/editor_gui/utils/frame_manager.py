import tkinter as tk
from tkinter import ttk
from typing import Callable, Any


class FrameManager(tk.LabelFrame):
    def __init__(self, master, name: str, on_create: Callable[..., Any]):
        super().__init__(master, text=name)
        self.on_create = on_create
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill='both', expand='yes')

    def create(self, name: str, *args, **kwargs):
        frame = ttk.Frame(self.notebook)
        item = self.on_create(frame, name, *args, **kwargs)
        item.pack(fill='both', expand=True)

        self.notebook.add(frame, text=name)
        self.notebook.select(frame)
