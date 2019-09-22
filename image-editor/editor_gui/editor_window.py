import tkinter as tk
from tkinter import messagebox

from editor_gui.editor_notebook import EditorNotebook
from editor_core.config.project import ProjectManager
from editor_core.config.editor import EditorManager
from editor_gui.event_bus import OPEN_FILE_BUS, OpenFileEvent, OPEN_PROJECT_BUS
from editor_gui.file_select import ask_open_project, ask_open_image, ask_open_dataset
from editor_gui.project_browser import ProjectBrowser
from editor_gui.utils.ui_utils import build_menu


class EditorWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.editor_config = EditorManager.load()
        self.iconbitmap('')

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{}x{}+5+5'.format(w - 20, h - 150))
        self.protocol("WM_DELETE_WINDOW", self._on_exit)
        self.init_menu()

        frame = tk.PanedWindow(orient=tk.HORIZONTAL)
        frame.pack(fill=tk.BOTH, expand=1)

        self.project_browser = ProjectBrowser(frame, ProjectManager(self.editor_config))
        frame.add(self.project_browser)

        self.notebook = EditorNotebook(frame, name='editor')
        frame.add(self.notebook)

    def init_menu(self):
        menu = {
            'File': {
                'New image': lambda: OPEN_FILE_BUS.on_next(
                    OpenFileEvent('image', name='editor')),
                'Open image': lambda: OPEN_FILE_BUS.on_next(
                    OpenFileEvent('image', path=ask_open_image(self.editor_config))),

                'New data': lambda: OPEN_FILE_BUS.on_next(
                    OpenFileEvent('data', name='data')),
                'Open data': lambda: OPEN_FILE_BUS.on_next(
                    OpenFileEvent('data', path=ask_open_dataset(self.editor_config))),

                'Open project': lambda: OPEN_PROJECT_BUS.on_next(ask_open_project(self.editor_config)),

                'Exit': self._on_exit

            },
            'Edit': {},
            'View': {},

            'Operator': {
                str(_()): {}
                for _ in EditorManager.plugin.operators()
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
