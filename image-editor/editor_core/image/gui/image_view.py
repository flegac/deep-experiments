import tkinter as tk

import rx.operators as ops
from PIL import ImageTk, Image
from rx.subject import Subject

from editor_api.data.data_source import DataSource
from editor_api.data.data_utils import DataUtils
from editor_core.image.gui.view_controller import ViewController


class ImageView(tk.Frame):
    MAX_REDRAW_PER_SEC = 1000

    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)
        self._redraw_bus = Subject()
        self._redraw_bus.pipe(
            ops.throttle_first(1. / ImageView.MAX_REDRAW_PER_SEC),
            # ops.debounce(1. / ImageView.MAX_REDRAW_PER_SEC),
        ).subscribe(on_next=lambda _: self._redraw(_))

        # canvas creation
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.pack(expand=True, fill="both")

        # image
        self.data = None
        self.image_id = None

        self.viewport_controller = ViewController(self.canvas, self.redraw)

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda _: self._redraw(None))
        for k, v in self.viewport_controller.bindings().items():
            self.canvas.bind(k, v)

    def mouse_image_coords(self):
        return self.viewport_controller.mouse_image_coords()

    def redraw(self, source: DataSource = None):
        if not isinstance(source, DataSource):
            source = None
        self._redraw_bus.on_next(source)

    def _redraw(self, source: DataSource = None):
        if source is not None:
            self.data = source.get_buffer()
        if self.image_id:
            self.canvas.delete(self.image_id)
        if self.data is None:
            return

        data = self.viewport_controller.viewport.apply(self.data)

        self.canvas.image = ImageTk.PhotoImage(image=Image.fromarray(data))
        self.image_id = self.canvas.create_image((0, 0), anchor=tk.NW, image=self.canvas.image)
        self.canvas.lower(self.image_id)  # set it into background


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageView(root)
    editor.redraw(DataUtils.random_source)
    editor.pack(fill='both', expand=True)
    root.mainloop()
