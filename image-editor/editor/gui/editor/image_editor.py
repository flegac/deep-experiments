import tkinter as tk
from enum import Enum

from PIL import ImageTk, Image

from editor.gui.editor.layer_editor import LayerEditor
from editor.gui.utils.hidden_scrollbar import HiddenScrollbar
from editor.plugins.core.datasource.cached_source import CachedSource
from editor.plugins.core.transforms.viewport import ViewportTransformer


# advanced version :
# https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan/48137257#48137257
# basic version :
# https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse


class ImageEvent(Enum):
    ON_VIEWPORT_CHANGE = 'on_viewport'
    ON_SOURCE_CHANGE = 'on_source_change'


class ImageEditor(tk.Frame):
    ZOOM_SPEED = 0.75

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # canvas creation
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Vertical and horizontal scrollbars for canvas
        vbar = HiddenScrollbar(self, orient='vertical', command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky='ns')
        hbar = HiddenScrollbar(self, orient='horizontal', command=self.canvas.xview)
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        # editors
        self.layer_editor = LayerEditor(self, self.on_source_change)
        self.layer_editor.grid(row=0, column=1, sticky='nsew')

        # image
        self.source = CachedSource(lambda: self.layer_editor.get_source())
        self.image = None
        self.image_id = None
        self.viewport = ViewportTransformer(self._viewport_provider)

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
        self.on_viewport_change()
        self.mouse_x = event.x
        self.mouse_y = event.y

    def zoom(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.viewport.zoom(self.ZOOM_SPEED)
        if event.num == 4 or event.delta == 120:
            self.viewport.zoom(1 / self.ZOOM_SPEED)
        self.on_viewport_change()

    def on_source_change(self):
        self.source.invalidate()
        self.layer_editor.visu_editor.update_data(self.source())
        self.redraw_canvas()

    def on_viewport_change(self):
        self.redraw_canvas()

    def redraw_canvas(self):
        self.update_debug()

        if self.image_id:
            self.canvas.delete(self.image_id)

        # extract data
        data = self.viewport(self.source())
        try:
            self.image = ImageTk.PhotoImage(image=Image.fromarray(data))
            self.image_id = self.canvas.create_image((0, 0), anchor=tk.NW, image=self.image)
            self.canvas.lower(self.image_id)  # set it into background
        except:
            pass

    def update_debug(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if self.debug_id:
            self.canvas.delete(self.debug_id)
        self.debug_id = self.canvas.create_text(5, 5, anchor='nw',
                                                text='canvas=({},{}) viewport={}'.format(w, h, self.viewport))

    def _viewport_provider(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        return w, h
