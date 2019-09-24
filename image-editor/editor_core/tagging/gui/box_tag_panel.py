import tkinter as tk

import pandas as pd

from editor_core.tagging.box_painter import TagBoxManager
from editor_core.files.gui.file_select import ask_open_image, ask_save_file


class BoxTagPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='tags')

        self.box_painter = TagBoxManager(self)
        self.box_painter.update_bus.subscribe(on_next=self.redraw)

        self.text = tk.StringVar()
        label = tk.Label(self, textvariable=self.text)
        label.pack(fill='both', expand=True, side=tk.TOP)

        button = tk.Button(
            self,
            text='Open',
            command=lambda: self.box_painter.load_dataset(pd.read_csv(ask_open_image()))
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Save',
            command=lambda: self.box_painter.save_dataset(ask_save_file())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Clear',
            command=lambda: self.box_painter.boxes.drop(self.box_painter.boxes.index, inplace=True)
        )
        button.pack(fill='both', expand=True, side=tk.RIGHT)
        self.redraw()

    def redraw(self, event=None):
        self.text.set('{} items'.format(self.box_painter.boxes.shape[0]))
        pass


if __name__ == '__main__':
    root = tk.Tk()
    editor = BoxTagPanel(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
