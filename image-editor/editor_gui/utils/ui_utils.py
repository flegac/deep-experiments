import tkinter as tk
from typing import Mapping, Union, Callable

MenuConfig = Mapping[str, Union[str, Mapping[str, str]]]


def build_menu(parent, config: MenuConfig) -> tk.Menu:
    menu = tk.Menu(parent)
    for label, commands in config.items():
        if isinstance(commands, Callable):
            menu.add_command(label=label, command=commands)
        else:
            sub_menu = tk.Menu(menu, tearoff=0)
            for cmd_label, command in commands.items():
                sub_menu.add_command(label=cmd_label, command=command)
            menu.add_cascade(label=label, menu=sub_menu)
    return menu


def add_popup(widget, menu: tk.Menu):
    def popup(event):
        try:
            menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            menu.grab_release()

    widget.bind('<Button-3>', popup)
