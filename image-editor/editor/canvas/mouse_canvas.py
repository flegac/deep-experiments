import tkinter as tk

import cv2
from PIL import ImageTk, Image

from editor.canvas.viewport import Viewport
from editor.hidden_scrollbar import HiddenScrollbar


# advanced version :
# https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan/48137257#48137257
# basic version :
# https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse


class MouseCanvas(tk.Frame):
    ZOOM_SPEED = 0.75

    def __init__(self, master):
        tk.Frame.__init__(self, master)

        # canvas creation
        self.canvas = tk.Canvas(self, width=600, height=400)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Vertical and horizontal scrollbars for canvas
        vbar = HiddenScrollbar(self, orient='vertical', command=self.canvas.yview)
        vbar.grid(row=0, column=1, sticky='ns')
        hbar = HiddenScrollbar(self, orient='horizontal', command=self.canvas.xview)
        hbar.grid(row=1, column=0, sticky='ew')

        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        # Make the canvas expandable
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.pack(fill="both", expand=True)

        # image
        self.viewport = Viewport()
        self.image = None
        self.image_id = None
        self.mouse_x = None
        self.mouse_y = None

        # help
        self.canvas.create_text(5, 10, anchor='nw', text='CTRL+Click : move image\nMouse Wheel : zoom image')
        self.debug_id = self.canvas.create_text(5, 50, anchor='nw', text='viewport={}'.format(self.viewport))

        # toolbox
        self.var = tk.BooleanVar()

        def update_contrast():
            self.viewport.with_contrast_stretching = self.var.get()
            self.redraw_canvas()

        tk.Checkbutton(self.canvas,
                       text='contrast stretching',
                       variable=self.var,
                       command=update_contrast).pack()

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda event: self.redraw_canvas())

        self.canvas.bind('<Control-ButtonPress-1>', self.move_from)
        self.canvas.bind('<Control-B1-Motion>', self.move_to)
        # linux scroll
        self.canvas.bind('<Button-4>', self.zoom)
        self.canvas.bind('<Button-5>', self.zoom)
        # windows scroll
        self.canvas.bind('<MouseWheel>', self.zoom)

    def open(self, path: str):
        data = cv2.imread(path)
        data = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)
        self.viewport.data = data
        self.redraw_canvas()

    def move_from(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        # self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        # self.canvas.scan_dragto(event.x, event.y, gain=1)
        dx = self.mouse_x - event.x
        dy = self.mouse_y - event.y
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.viewport.move(dx, dy)
        self.redraw_canvas()

    def zoom(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.viewport.zoom(self.ZOOM_SPEED)
        if event.num == 4 or event.delta == 120:
            self.viewport.zoom(1 / self.ZOOM_SPEED)
        self.redraw_canvas()

    def update_debug(self, w: int, h: int):
        if self.debug_id:
            self.canvas.delete(self.debug_id)
        self.debug_id = self.canvas.create_text(2, 30, anchor='nw',
                                                text='canvas=({},{}) viewport={}'.format(w, h, self.viewport))

    def redraw_canvas(self):
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        self.update_debug(w, h)

        if self.image_id:
            self.canvas.delete(self.image_id)

        # extract data
        data = self.viewport.get_buffer(w, h)
        try:
            self.image = ImageTk.PhotoImage(image=Image.fromarray(data))
            self.image_id = self.canvas.create_image((0, 0), anchor=tk.NW, image=self.image)
            self.canvas.lower(self.image_id)  # set it into background
        except:
            pass


if __name__ == "__main__":
    root = tk.Tk()
    canvas = MouseCanvas(root)
    canvas.open('D:\\Datasets\\change\\20190802_export_s2_it1\\images\\nouakchott_1_s2_0.tif')

    root.mainloop()
