import tkinter as tk
from typing import Callable, Any

from editor_gui.file_select import ask_open_image, ask_save_file


class FileToolbox(tk.LabelFrame):
    def __init__(self, master: tk.Widget, open_func: Callable[[str], Any], save_func: Callable[[str], Any]):
        tk.LabelFrame.__init__(self, master, text='files')

        button = tk.Button(
            self,
            text='Open',
            command=lambda: open_func(ask_open_image())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Save',
            command=lambda: save_func(ask_save_file())
        )
        button.pack(fill='both', expand=True, side=tk.RIGHT)


if __name__ == '__main__':
    root = tk.Tk()
    editor = FileToolbox(root, None, None)
    editor.pack(fill='both', expand=True)
    root.mainloop()
