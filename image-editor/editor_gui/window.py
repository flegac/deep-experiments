import tkinter as tk
from tkinter import messagebox

from editor_gui.dataset_editor import DatasetEditor
from editor_gui.event_bus import IMAGE_OPEN_BUS, DATASET_OPEN_BUS, TEXT_OPEN_BUS
from editor_gui.image.image_editor import ImageEditor
from editor_gui.project_browser import ProjectBrowser
from editor_gui.text_editor import TextEditor
from editor_gui.utils.frame_manager import FrameManager
from editor_gui.utils.ui_utils import build_menu, MenuConfig


class Win(tk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('')

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{}x{}+5+5'.format(w - 20, h - 150))
        self.protocol("WM_DELETE_WINDOW", self._on_exit)

        frame = tk.PanedWindow(orient=tk.HORIZONTAL)
        frame.pack(fill=tk.BOTH, expand=1)

        self.browser = ProjectBrowser(frame)
        frame.add(self.browser)

        self.editor = FrameManager(frame, name='editor')
        self.editor.register(IMAGE_OPEN_BUS, ImageEditor)
        self.editor.register(DATASET_OPEN_BUS, DatasetEditor)
        self.editor.register(TEXT_OPEN_BUS, TextEditor)

        IMAGE_OPEN_BUS.on_next(('---', None))

        frame.add(self.editor)

    def config_menu(self, config: MenuConfig):
        self.config(menu=build_menu(self, config))

    def _on_exit(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit ?"):
            self.destroy()

    def help(self):
        messagebox.showinfo("Help", """
        Click + mouse : move image
        Mouse wheel : zoom image
        """)
