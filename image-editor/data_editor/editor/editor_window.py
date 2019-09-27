import tkinter as tk
from tkinter import messagebox

from data_editor.editor.editor_notebook import EditorNotebook
from data_editor.editor_config import EditorManager
from data_editor.project.project_browser import ProjectBrowser
from data_editor.project_config import ProjectManager
from data_editor.utils.file_select import ask_open_project, ask_open_image, ask_open_dataset
from data_editor.utils.ui_utils import build_menu
from data_toolbox.buffer.buffer_factory import ImageFactory
from data_toolbox.table.table_source import TableSource


class EditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('')

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{}x{}+0+0'.format(w - 150, h - 150))
        self.protocol("WM_DELETE_WINDOW", self._on_exit)
        self.init_menu()

        frame = tk.PanedWindow(orient=tk.HORIZONTAL)
        frame.pack(fill=tk.BOTH, expand=1)

        self.project_browser = ProjectBrowser(
            frame, ProjectManager(),
            on_open=lambda path: self.notebook.request_update(path))
        frame.add(self.project_browser)

        self.notebook = EditorNotebook(frame, name='editor')
        frame.add(self.notebook)

    def init_menu(self):
        menu = {
            'File': {
                'New image': lambda: self.notebook.request_update(ImageFactory.empty),
                'Open image': lambda: self.notebook.request_update(ImageFactory.from_rgb(ask_open_image())),

                'New data': lambda: self.notebook.request_update(TableSource()),
                'Open data': lambda: self.notebook.request_update(TableSource().load(ask_open_dataset())),

                'New project': lambda: self.project_browser.create_project(),
                'Open project': lambda: self.project_browser.request_update(ask_open_project()),

                'Exit': self._on_exit

            },
            'Edit': {},
            'View': {},

            'Operator': {
                str(_()): {}
                for _ in EditorManager.plugin.operators()
            },
            'Mixer': {
                'Blend': {}
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
