import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from editor.canvas.mouse_canvas import MouseCanvas


class ImageManager(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="image editor")
        self.pack(fill="both", expand="yes")
        self.notebook = ttk.Notebook(self, width=600, height=400)
        self.notebook.pack(fill="both", expand="yes")
        self.editors = []

    def open(self):
        path = askopenfilename(
            title="Open image",
            filetypes=[
                ('tiff files', '.tif'),
                ('png files', '.png'),
                ('all files', '.*')
            ]
        )
        frame = ttk.Frame(self.notebook)
        editor = MouseCanvas(frame)
        editor.open(path)
        self.editors.append(editor)
        self.notebook.add(frame, text=os.path.basename(path))
