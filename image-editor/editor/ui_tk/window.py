import tkinter as ttk
from tkinter import messagebox
from typing import Mapping, Union, Callable

from editor.ui_tk.editor_manager import EditorManager

MenuConfig = Mapping[str, Union[str, Mapping[str, str]]]


class Win(ttk.Tk):
    def __init__(self):
        super().__init__()
        w, h = self.winfo_screenwidth(), self.winfo_screenheight()

        self.geometry('{}x{}+5+5'.format(w - 20, h - 150))
        self.editor = EditorManager(self)

        self.protocol("WM_DELETE_WINDOW", self._on_exit)

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
