import os
import tkinter as tk

import cv2

from data_editor.editor.editor_config import EditorManager
from data_editor.project.project_config import ProjectManager
from data_editor.utils.file_select import ask_open_file
from data_toolbox.model.model_source import ModelSource
from data_toolbox.model.model_display_worker import ModelDisplayWorker
from data_toolbox.model.model_viewer import ModelViewer


class ModelPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='model')

        self.text = tk.StringVar(value='<no model>')
        tk.Label(self, textvariable=self.text).pack(fill=tk.X, expand=True, side=tk.TOP)

        self.model = None
        tk.Button(self, text='Predict', command=lambda: self.predict()).pack(fill=tk.X, expand=True, side=tk.LEFT)
        tk.Button(self, text='generate', command=lambda: self.generate()).pack(fill=tk.X, expand=True, side=tk.LEFT)

    def set_source(self, model: ModelSource):
        self.model = model
        self.text.set(str(self.model))

    def predict(self):
        if self.model is None:
            self.text.set('load a model first !')
        path = ask_open_file()
        data = cv2.imread(path)

        manager = EditorManager.load()
        target_path = os.path.join(str(manager.root_path), manager.project,os.path.basename(path))

        ModelViewer(self.model,target_path).apply(data)

    def generate(self):
        if self.model is None:
            self.text.set('load a model first !')

        manager = EditorManager.load()
        path = os.path.join(str(manager.root_path), manager.project)

        ModelDisplayWorker(self.model).work(path)


if __name__ == '__main__':
    root = tk.Tk()
    ModelPanel(root).pack(fill='both', expand=True)
    root.mainloop()
