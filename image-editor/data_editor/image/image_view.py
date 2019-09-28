import tkinter as tk

import rx.operators as ops
from PIL import ImageTk, Image
from rx.subject import Subject

from data_editor.image.view_controller import ViewController
from data_toolbox.data.data_source import DataSource
from data_toolbox.image.buffer_factory import ImageFactory


class ImageView(tk.Frame):
    MAX_REDRAW_PER_SEC = 1000

    def __init__(self, master: tk.Widget, width: int = 600, height: int = 400):
        tk.Frame.__init__(self, master)
        self._source_change_bus = Subject()
        self._source_change_bus.pipe(
            ops.throttle_first(1. / ImageView.MAX_REDRAW_PER_SEC),
            # ops.debounce(1. / ImageView.MAX_REDRAW_PER_SEC),
        ).subscribe(on_next=lambda _: self._redraw(_))

        # canvas creation
        self.canvas = tk.Canvas(self, width=width, height=height)
        self.canvas.pack(expand=True, fill="both")

        # image
        self.data = None
        self.image_id = None

        self.viewport_controller = ViewController(self.canvas, self.set_source)

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda _: self._redraw(None))
        for k, v in self.viewport_controller.bindings().items():
            self.canvas.bind(k, v)

    def mouse_image_coords(self):
        return self.viewport_controller.mouse_image_coords()

    def reset_viewport(self):
        self.viewport_controller.viewport.zoom_factor = 0
        self.viewport_controller.viewport.x = 0
        self.viewport_controller.viewport.y = 0

    def set_source(self, source: DataSource = None):
        self._source_change_bus.on_next(source)

    def _redraw(self, source: DataSource = None):
        if source is not None:
            self.data = source.get_data()
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
    editor.set_source(ImageFactory.random)
    editor.pack(fill='both', expand=True)
    root.mainloop()
