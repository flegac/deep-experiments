import tkinter as tk
from tkinter.colorchooser import askcolor
from typing import Tuple, Callable, Any

from rx.subject import Subject

from data_editor.utils.toolbox import FileToolbox
from data_toolbox.tagging.box_tag_source import BoxTagSource


class BoxTagPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='tagging')
        self._observer = Subject()
        self.subscribe(self._redraw)

        self.source = BoxTagSource()

        self.brush_size = tk.IntVar(value=8)
        self.brush_tag = tk.IntVar(value=0)
        self.text = tk.StringVar()

        tk.Label(self, textvariable=self.text).pack(fill='both', expand=True, side=tk.TOP)

        brush = tk.LabelFrame(self, text='brush')
        brush.pack(fill='both', expand=True, side=tk.TOP)
        brush_size = tk.Frame(brush)
        brush_size.pack(fill=tk.X, expand=False, side=tk.TOP)

        tk.Label(brush_size, text='size').pack(fill=None, expand=False, side=tk.LEFT)
        tk.Scale(brush_size, variable=self.brush_size, from_=1, to=1024, orient=tk.HORIZONTAL).pack(fill=None,
                                                                                                    expand=False,
                                                                                                    side=tk.RIGHT)
        brush_tag = tk.Frame(brush)
        brush_tag.pack(fill=tk.X, expand=False, side=tk.TOP)

        tk.Label(brush_tag, text='tag').pack(fill=None, expand=False, side=tk.LEFT)
        tk.Scale(brush_tag, variable=self.brush_tag, from_=0, to=128, orient=tk.HORIZONTAL).pack(fill=None,
                                                                                                 expand=False,
                                                                                                 side=tk.RIGHT)

        FileToolbox(
            self,
            lambda path: (self.source.load(path), self._request_update()),
            lambda path: self.source.save(path)
        ).pack(expand=True, fill='both', side=tk.BOTTOM)

        tk.Button(
            self,
            text='Clear',
            command=lambda: (self.source.clear(), self._request_update())
        ).pack(fill='both', expand=True, side=tk.LEFT)

        tk.Button(
            self,
            text='Refresh',
            command=self._request_update
        ).pack(fill='both', expand=True, side=tk.BOTTOM)

        tk.Button(
            self,
            text='Color',
            command=self.choose_color
        ).pack(fill='both', expand=True, side=tk.BOTTOM)
        self._redraw()

    def subscribe(self, on_next: Callable[[Any], None]):
        self._observer.subscribe(on_next)

    def choose_color(self):
        rgb_color, web_color = askcolor(parent=self, initialcolor=(255, 0, 0))

    def create_box(self, center: Tuple[int, int]):
        self.source.add_box(center, radius=self.brush_size.get(), tag=self.brush_tag.get())
        self._request_update()

    def _request_update(self):
        self._observer.on_next(self.source)

    def _redraw(self, event=None):
        self.text.set('{} items'.format(self.source.get_table().shape[0]))


if __name__ == '__main__':
    root = tk.Tk()
    editor = BoxTagPanel(root)
    editor.pack(fill='both', expand=True)
    root.mainloop()
