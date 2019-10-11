import os
import tkinter as tk

import cv2

from data_editor.editor_config import EditorManager
from data_editor.utils.file_select import ask_open_file
from data_toolbox.worker.model_display_worker import ModelDisplayWorker
from data_toolbox.worker.model_viewer import ModelViewer


class ModelPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='model')

        self.text = tk.StringVar(value='<no model>')
        tk.Label(self, textvariable=self.text).pack(fill=tk.X, expand=True, side=tk.TOP)

        self.model_viewer = None
        tk.Button(self, text='Load', command=self.load_model).pack(fill=tk.X, expand=True, side=tk.LEFT)
        # tk.Button(self, text='Show', command=lambda: self.model.show()).pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(self, text='Predict', command=lambda: self.predict()).pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(self, text='generate', command=lambda: self.generate()).pack(fill=tk.X, expand=True, side=tk.LEFT)

    def predict(self):
        if self.model_viewer is None:
            self.text.set('load a model first !')
        path = ask_open_file()
        data = cv2.imread(path)
        self.model_viewer.apply(data)

    def generate(self):
        if self.model_viewer is None:
            self.text.set('load a model first !')

        manager = EditorManager.load()
        path = os.path.join(str(manager.root_path), manager.project)

        ModelDisplayWorker(self.model_viewer.model).work(path)

    def load_model(self):
        path = ask_open_file()
        self.model_viewer = ModelViewer(path)
        self.text.set(os.path.basename(path))


if __name__ == '__main__':
    root = tk.Tk()
    ModelPanel(root).pack(fill='both', expand=True)
    root.mainloop()
