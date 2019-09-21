import tkinter as ttk
from tkinter import messagebox
from typing import Mapping, Union, Callable

from editor_gui.dataset_editor import DatasetEditor
from editor_gui.text_editor import TextEditor
from editor_gui.events import IMAGE_OPEN_BUS, DATASET_OPEN_BUS, TEXT_OPEN_BUS
from editor_gui.image.image_editor import ImageEditor
from editor_gui.project_browser import ProjectBrowser
from editor_gui.utils.frame_manager import FrameManager

MenuConfig = Mapping[str, Union[str, Mapping[str, str]]]


class Win(ttk.Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap('')

        w, h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry('{}x{}+5+5'.format(w - 20, h - 150))
        self.protocol("WM_DELETE_WINDOW", self._on_exit)

        frame = ttk.PanedWindow(orient=ttk.HORIZONTAL)
        frame.pack(fill=ttk.BOTH, expand=1)

        self.browser = ProjectBrowser(frame)
        frame.add(self.browser)

        self.editor = FrameManager(frame, name='editor')
        self.editor.register(IMAGE_OPEN_BUS, ImageEditor)
        self.editor.register(DATASET_OPEN_BUS, DatasetEditor)
        self.editor.register(TEXT_OPEN_BUS, TextEditor)

        IMAGE_OPEN_BUS.on_next(('---', None))

        frame.add(self.editor)

    def config_menu(self, config: MenuConfig):
        top_menu = ttk.Menu(self)

        for label, commands in config.items():
            if isinstance(commands, Callable):
                top_menu.add_command(label=label, command=commands)
            else:
                sub_menu = ttk.Menu(top_menu, tearoff=0)
                for cmd_label, command in commands.items():
                    sub_menu.add_command(label=cmd_label, command=command)
                top_menu.add_cascade(label=label, menu=sub_menu)
        self.config(menu=top_menu)

    def _on_exit(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit ?"):
            self.destroy()

    def help(self):
        messagebox.showinfo("Help", """
        Click + mouse : move image
        Mouse wheel : zoom image
        """)
