import os
import tkinter as tk

import cv2

from data_editor.utils.file_select import ask_open_file
from data_toolbox.image.operator.model_viewer import ModelViewer


class ModelPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='model')

        self.text = tk.StringVar(value='<no model>')
        tk.Label(self, textvariable=self.text).pack(fill=tk.X, expand=True, side=tk.TOP)

        self.model = None
        tk.Button(self, text='Load', command=self.load_model).pack(fill=tk.X, expand=True, side=tk.LEFT)
        # tk.Button(self, text='Show', command=lambda: self.model.show()).pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(self, text='Predict', command=lambda: self.predict()).pack(fill=tk.X, expand=True, side=tk.LEFT)

    def predict(self):
        if self.model is None:
            self.text.set('load a model first !')
        path = ask_open_file()
        data = cv2.imread(path)
        self.model.apply(data)

    def load_model(self):
        path = ask_open_file()
        self.model = ModelViewer(path)
        self.text.set(os.path.basename(path))


if __name__ == '__main__':
    root = tk.Tk()
    ModelPanel(root).pack(fill='both', expand=True)
    root.mainloop()
