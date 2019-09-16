import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from typing import List

from editor.ui_tk.image_editor import ImageEditor


class EditorManager(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="image editor")
        self.pack(fill="both", expand="yes")
        self.notebook = ttk.Notebook(self, width=800, height=640)
        self.notebook.pack(fill="both", expand="yes")
        self.editors = []

    def open(self):
        paths = askopenfilenames(
            title="Open image",
            filetypes=[
                ('tiff files', '.tif'),
                ('png files', '.png'),
                ('all files', '.*')
            ]
        )
        # self.open_files(paths)
        for _ in paths:
            self.open_file(_)

    def open_file(self, path: str):
        frame = ttk.Frame(self.notebook)
        editor = ImageEditor(frame)
        editor.open(path)
        self.editors.append(editor)
        self.notebook.add(frame, text=os.path.basename(path))

    def open_files(self, paths: List[str]):
        frame = ttk.Frame(self.notebook)
        editor = ImageEditor(frame)
        for _ in paths:
            editor.open(_)
        self.editors.append(editor)
        self.notebook.add(frame, text=os.path.basename(paths[0]))
