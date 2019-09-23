import tkinter as tk

import rx.operators as ops
from PIL import ImageTk, Image
from rx.subject import Subject

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataSource
from editor_api.data.data_utils import DataUtils
from editor_gui.image.view.paint_controller import PaintController
from editor_gui.image.view.view_controller import ViewportController
from editor_gui.utils.hidden_scrollbar import HiddenScrollbar


class ImageView(tk.Frame):
    MAX_REDRAW_PER_SEC = 1000

    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)

        # redraw bus
        self.redraw_bus = Subject()
        self.redraw_bus.pipe(
            ops.throttle_first(1. / ImageView.MAX_REDRAW_PER_SEC),
            # ops.debounce(1. / ImageView.MAX_REDRAW_PER_SEC),

        ).subscribe(on_next=lambda _: self.redraw_canvas())

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # canvas creation
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky='nsew')
        vbar = HiddenScrollbar(self, orient='vertical', command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky='ns')
        hbar = HiddenScrollbar(self, orient='horizontal', command=self.canvas.xview)
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        # image
        self.data = None
        self.image = None
        self.image_id = None

        self.viewport_controller = ViewportController(self.canvas, self.redraw_bus)
        self.viewport_controller.bind()

        self.paint_controller = PaintController(self)

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda _: self.redraw_canvas())
        self.bind_all('k', lambda _: self.viewport_controller.unbind_canvas())
        self.paint_controller.bind()

    def get_data(self, data_source: DataSource = None) -> Buffer:
        if data_source is not None:
            self.data = data_source.get_buffer()
        return self.data

    def on_source_change(self, source: DataSource):
        self.get_data(source)
        self.redraw_bus.on_next(source)

    def redraw_canvas(self):
        if self.image_id:
            self.canvas.delete(self.image_id)

        raw_data = self.get_data()
        self.paint_controller.apply(self)
        if raw_data is None:
            return
        data = self.viewport_controller.viewport.apply(raw_data)

        self.image = ImageTk.PhotoImage(image=Image.fromarray(data))
        self.image_id = self.canvas.create_image((0, 0), anchor=tk.NW, image=self.image)
        self.canvas.lower(self.image_id)  # set it into background


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageView(root)
    editor.on_source_change(DataUtils.random_source)
    editor.pack(fill='both', expand=True)
    root.mainloop()
