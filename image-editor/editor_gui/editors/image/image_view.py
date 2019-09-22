import tkinter as tk

from PIL import ImageTk, Image
from rx import operators
from rx.subject import Subject

from editor_api.data.data_core import DataSource
from editor_api.data.data_utils import DataUtils
from editor_core.viewport import ViewportOperator
from editor_gui.utils.hidden_scrollbar import HiddenScrollbar


class ImageView(tk.Frame):
    ZOOM_SPEED = 0.75
    MAX_REDRAW_PER_SEC = 24

    def __init__(self, master: tk.Widget):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.redraw_bus = Subject()
        self.redraw_bus.pipe(
            operators.throttle_first(1. / ImageView.MAX_REDRAW_PER_SEC)
        ).subscribe(on_next=lambda _: self.redraw_canvas())

        # canvas creation
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Vertical and horizontal scrollbars for canvas
        vbar = HiddenScrollbar(self, orient='vertical', command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky='ns')
        hbar = HiddenScrollbar(self, orient='horizontal', command=self.canvas.xview)
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        # image
        self.data = DataUtils.empty_source.get_buffer()
        self.image = None
        self.image_id = None
        self.viewport = ViewportOperator(self.viewport_size)

        # help
        self.debug_id = self.canvas.create_text(5, 60, anchor='nw', text='')

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda event: self.redraw_canvas())

        self.mouse_x = None
        self.mouse_y = None
        self.canvas.bind('<ButtonPress-1>', self.start_move)
        self.canvas.bind('<B1-Motion>', self.move)
        # linux scroll
        self.canvas.bind('<Button-4>', self.zoom)
        self.canvas.bind('<Button-5>', self.zoom)
        # windows scroll
        self.canvas.bind('<MouseWheel>', self.zoom)

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
        self.redraw_bus.on_next({})

    def zoom(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.viewport.zoom(self.ZOOM_SPEED)
        if event.num == 4 or event.delta == 120:
            self.viewport.zoom(1 / self.ZOOM_SPEED)
        self.redraw_bus.on_next({})

    def read_data(self, data_source: DataSource = None):
        if data_source is not None:
            self.data = data_source.get_buffer()
        return self.data

    def viewport_size(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        return w, h

    def on_source_change(self, source: DataSource):
        self.read_data(source)
        self.redraw_bus.on_next(None)

    def redraw_canvas(self):

        if self.image_id:
            self.canvas.delete(self.image_id)

        raw_data = self.read_data()
        data = self.viewport.apply(raw_data)

        self.image = ImageTk.PhotoImage(image=Image.fromarray(data))
        self.image_id = self.canvas.create_image((0, 0), anchor=tk.NW, image=self.image)
        self.canvas.lower(self.image_id)  # set it into background


if __name__ == '__main__':
    root = tk.Tk()
    editor = ImageView(root)
    editor.on_source_change(DataUtils.empty_source)
    editor.pack(fill='both', expand=True)
    root.mainloop()