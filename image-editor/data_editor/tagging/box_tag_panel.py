import tkinter as tk
from typing import Tuple

from rx.subject import Subject

from data_editor.utils.file_toolbox import FileToolbox
from data_toolbox.tagging.box_tag_source import BoxTagSource


class BoxTagPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='tags')
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self._redraw)

        self.source = BoxTagSource()
        self.brush_size = 8

        self.text = tk.StringVar()
        label = tk.Label(self, textvariable=self.text)
        label.pack(fill='both', expand=True, side=tk.TOP)

        self.file_box = FileToolbox(self,
                                    lambda path: (self.source.load(path), self.request_update()),
                                    lambda path: self.source.save(path))
        self.file_box.pack(expand=True, fill='both', side=tk.BOTTOM)

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
