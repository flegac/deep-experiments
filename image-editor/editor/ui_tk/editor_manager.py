import os
import tkinter as tk
from tkinter import ttk

from editor.ui_tk.image_editor import ImageEditor
from editor.ui_tk.utils.ui_utils import dataset_selection


class EditorManager(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="image editor")
        self.pack(fill="both", expand="yes")
        self.notebook = ttk.Notebook(self, width=800, height=640)
        self.notebook.pack(fill="both", expand="yes")
        self.editors = []

    def open(self):
        paths = dataset_selection()
        for _ in paths:
            self.open_file(_)

    def open_file(self, path: str):
        frame = ttk.Frame(self.notebook)
        editor = ImageEditor(frame, path)
        self.editors.append(editor)
        self.notebook.add(frame, text=os.path.basename(path))
        self.notebook.select(frame)
