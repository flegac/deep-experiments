import tkinter as tk
from typing import Tuple

from rx.subject import Subject

from editor_core.files.gui.file_select import ask_open_image, ask_save_file
from editor_core.tagging.box_table_source import BoxTableSource


class BoxTagPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='tags')
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)

        self.source = BoxTableSource()
        self.brush_size = 8

        self.text = tk.StringVar()
        label = tk.Label(self, textvariable=self.text)
        label.pack(fill='both', expand=True, side=tk.TOP)

        button = tk.Button(
            self,
            text='Open',
            command=lambda: (self.source.load(ask_open_image()), self.request_update())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Save',
            command=lambda: self.source.save(ask_save_file())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Clear',
            command=lambda: (self.source.clear(), self.request_update())
        )
        button.pack(fill='both', expand=True, side=tk.LEFT)

        button = tk.Button(
            self,
            text='Refresh',
            command=self.request_update
        )
        button.pack(fill='both', expand=True, side=tk.BOTTOM)
        self._redraw()

    def create_box(self, center: Tuple[int, int]):
        self.source.add_box(center, self.brush_size, tag=-1)
        self.request_update()

    def request_update(self):
        self.update_bus.on_next(self.source)

    def _redraw(self, event=None):
        self.text.set('{} items'.format(self.source.get_table().shape[0]))


if __name__ == '__main__':
    root = tk.Tk()
    editor = BoxTagPanel(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
