import tkinter as tk
from typing import Callable, Any

from data_editor.utils.file_select import ask_open_image, ask_save_file
from data_editor.utils.generic_toolbox import GenericToolbox


class FileToolbox(GenericToolbox):

    def __init__(self, master: tk.Widget, open_func: Callable[[str], Any], save_func: Callable[[str], Any]):
        super().__init__(master, {
            'Open': lambda: open_func(ask_open_image()),
            'Save': lambda: save_func(ask_save_file())
        })


if __name__ == '__main__':
    root = tk.Tk()
    editor = FileToolbox(root, None, None)
    editor.pack(fill='both', expand=True)
    root.mainloop()
