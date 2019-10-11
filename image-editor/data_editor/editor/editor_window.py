import tkinter as tk
from tkinter import messagebox

from data_editor.editor.editor_config import EditorManager
from data_editor.editor.editor_panel import EditorPanel
from data_editor.image.image_files import ask_open_image
from data_editor.model.model_files import ask_open_model
from data_editor.project.project_browser import ProjectBrowser
from data_editor.project.project_files import ask_open_project
from data_editor.table.table_files import ask_open_table
from data_editor.utils.ui_utils import build_menu
from data_toolbox.image.buffer_factory import ImageFactory
from data_toolbox.model.model import Model
from data_toolbox.model.model_source import ModelSource
from data_toolbox.table.table_source import TableSource


class EditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('')

        self.protocol("WM_DELETE_WINDOW", self._on_exit)
        self.init_menu()

        self.project_browser = ProjectBrowser(self, width=250)
        self.project_browser.pack(fill=tk.BOTH, expand=False, side=tk.LEFT)

        self.editor = EditorPanel(self)
        self.editor.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

        # self.update_idletasks()
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{}x{}+0+0'.format(w - 150, h - 150))

        # events
        self.project_browser.subscribe(lambda path: self.editor.request_view_update(path))

    def init_menu(self):
        menu = {
            'Project': {
                'New': lambda: self.project_browser.create_project(),
                'Open': lambda: self.project_browser.open_project(ask_open_project()),
                'Exit': self._on_exit

            },
            'Image': {
                'New': lambda: self.project_browser.source_browser.add_source(ImageFactory.empty),
                'Open': lambda: self.project_browser.source_browser.add_source(ImageFactory.from_rgb(ask_open_image())),
            },

            'Table': {
                'New': lambda: self.project_browser.source_browser.add_source(TableSource()),
                'Open': lambda: self.project_browser.source_browser.add_source(TableSource().load(ask_open_table())),
            },

            'Model': {
                'New': lambda: self.project_browser.source_browser.add_source(ModelSource(Model.from_scratch())),
                'Open': lambda: self.project_browser.source_browser.add_source(
                    ModelSource(Model.from_h5(ask_open_model()))),
            },

            'Operator': {
                str(_()): {}
                for _ in EditorManager.plugin.operators()
            },
            'Mixer': {
                'Blend': {},
                'Compare': {}
            },

            'Help': {
                'Help': self.help,
                'About': {}
            }
        }
        self.config(menu=build_menu(self, menu))

    def _on_exit(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit ?"):
            self.destroy()

    def help(self):
        messagebox.showinfo(
            "Help",
            """
Click + mouse : move image
Mouse wheel : zoom image
"""
        )


if __name__ == '__main__':
    EditorWindow().mainloop()
