import tkinter as ttk
from typing import Mapping, Union

from editor.ui_tk.editor_manager import EditorManager

MenuConfig = Mapping[str, Union[str, Mapping[str, str]]]


class Win(ttk.Tk):
    def __init__(self):
        super().__init__()
        self.editor = EditorManager(self)

    def config_menu(self, config: MenuConfig):
        top_menu = ttk.Menu(self)

        for label, commands in config.items():
            sub_menu = ttk.Menu(top_menu, tearoff=0)
            for cmd_label, command in commands.items():
                sub_menu.add_command(label=cmd_label, command=command)

            top_menu.add_cascade(label=label, menu=sub_menu)
        self.config(menu=top_menu)
