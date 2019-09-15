import tkinter as tk
from typing import Mapping, Union

from editor.image_manager import ImageManager

MenuConfig = Mapping[str, Union[str, Mapping[str, str]]]


class Win(tk.Tk):
    def __init__(self):
        super().__init__()
        self.editor = ImageManager(self)

    def config_menu(self, config: MenuConfig):
        top_menu = tk.Menu(self)

        for label, commands in config.items():
            sub_menu = tk.Menu(top_menu, tearoff=0)
            for cmd_label, command in commands.items():
                sub_menu.add_command(label=cmd_label, command=command)

            top_menu.add_cascade(label=label, menu=sub_menu)
        self.config(menu=top_menu)
