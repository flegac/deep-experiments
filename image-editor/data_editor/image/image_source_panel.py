import tkinter as tk
from typing import Callable, Any

import cv2
from rx.subject import Subject

from data_editor.utils.toolbox import FileToolbox
from data_toolbox.data.data_source import DataSource
from data_toolbox.image.buffer_factory import ImageFactory
from data_toolbox.image.source.buffer_source import BufferSource


class ImageSourcePanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='buffer', width=100, height=50)
        self._observer = Subject()

        self._source = None
        self.text = tk.StringVar()
        tk.Label(
            self,
            textvariable=self.text
        ).pack(fill='both', expand=True, side=tk.TOP)
        FileToolbox(
            self,
            lambda _: self.set_source(ImageFactory.from_rgb(_)),
            self.save_image
        ).pack(expand=True, fill='both', side=tk.BOTTOM)

        self.set_source(ImageFactory.empty)

    def subscribe(self, on_next: Callable[[Any], None]):
        return self._observer.subscribe(on_next=on_next)

    @property
    def source(self) -> DataSource:
        return self._source

    @property
    def source_descriptor(self):
        buffer = self.source.get_data()
        return '{name} {shape[1]}x{shape[0]} {type}'.format(name=str(self._source),
                                                            shape=buffer.shape,
                                                            type=buffer.dtype)

    def set_source(self, source: BufferSource = None):
        if source is None:
            return
        self._source = source
        self.text.set('{}'.format(self.source_descriptor))
        self._observer.on_next(self.source)

    def save_image(self, path: str = None):
        if path is None or path == '':
            return
        print('save to {}'.format(path))
        img = self.source.get_data()
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imwrite(path, img)


if __name__ == '__main__':
    root = tk.Tk()
    ImageSourcePanel(root).pack(fill="both", expand=True, side=tk.BOTTOM)
    root.mainloop()
