import tkinter as tk

import cv2
from PIL import ImageTk, Image
from rx import operators
from rx.subject import Subject

from editor_api.data.buffer import Buffer
from editor_api.data.data_core import DataSource
from editor_api.data.data_utils import DataUtils
from editor_core.viewport import ViewportOperator
from editor_gui.utils.hidden_scrollbar import HiddenScrollbar


class ImageView(tk.Frame):
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)

        # redraw bus
        self.redraw_bus = Subject()
        self.redraw_bus.pipe(
            operators.throttle_first(1. / ImageView.MAX_REDRAW_PER_SEC)
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
        self.canvas.bind('<Configure>', lambda event: self.redraw_canvas())
        self.bind_all('k', lambda _: self.viewport_controller.unbind_canvas())
        self.bind_all('a', self.paint_controller.paint)

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
        data = self.viewport_controller.viewport.apply(raw_data)

        self.image = ImageTk.PhotoImage(image=Image.fromarray(data))
        self.image_id = self.canvas.create_image((0, 0), anchor=tk.NW, image=self.image)
        self.canvas.lower(self.image_id)  # set it into background


class PaintController(object):
    def __init__(self, view: ImageView):
        self.view = view
        self.brush_size = 8
        self.brush_func = cv2.rectangle
        self.color = (0, 255, 0)
        self.thickness = 1

    def paint(self, event=None):
        img_x, img_y = self.view.viewport_controller.mouse_image_coords()
        self.view.data = cv2.rectangle(
            self.view.data,
            (img_x - self.brush_size, img_y - self.brush_size),
            (img_x + self.brush_size, img_y + self.brush_size),
            color=(0, 255, 0),
            thickness=1
        )
        self.view.redraw_bus.on_next(None)


class ViewportController(object):
    ZOOM_SPEED = 0.75
    EVENTS = [
        '<ButtonPress-1>',
        '<B1-Motion>',
        '<Button-4>',
        '<Button-5>',
        '<MouseWheel>',
        '<Key>'
    ]

    def __init__(self, canvas, redraw_bus: Subject):
        self.canvas = canvas
        self.redraw_bus = redraw_bus

        self.viewport = ViewportOperator(self.viewport_size)
        self.mouse_x = None
        self.mouse_y = None

    def mouse_image_coords(self):
        root = self.canvas.master
        z = self.viewport.zoom_factor
        mouse_x = int((root.winfo_pointerx() - root.winfo_rootx()) / z)
        mouse_y = int((root.winfo_pointery() - root.winfo_rooty()) / z)
        img_x = mouse_x + self.viewport.x
        img_y = mouse_y + self.viewport.y
        return img_x, img_y

    def bind(self):
        self.canvas.bind('<ButtonPress-1>', self.start_move)
        self.canvas.bind('<B1-Motion>', self.move)
        # linux scroll
        self.canvas.bind('<Button-4>', self.zoom)
        self.canvas.bind('<Button-5>', self.zoom)
        # windows scroll
        self.canvas.bind('<MouseWheel>', self.zoom)

    def unbind_canvas(self):
        if self.canvas is not None:
            for _ in self.EVENTS:
                self.canvas.unbind(_)
            self.canvas = None

    def viewport_size(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        return w, h

    def start_move(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def move(self, event):
        # self.canvas.scan_dragto(event.x, event.y, gain=1)
        dx = (self.mouse_x - event.x)
        dy = (self.mouse_y - event.y)
        self.viewport.move(dx, dy)
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.redraw_bus.on_next(None)

    def zoom(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.viewport.zoom(self.ZOOM_SPEED)
        if event.num == 4 or event.delta == 120:
            self.viewport.zoom(1 / self.ZOOM_SPEED)
        self.redraw_bus.on_next(None)


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageView(root)
    editor.on_source_change(DataUtils.random_source)
    editor.pack(fill='both', expand=True)
    root.mainloop()
