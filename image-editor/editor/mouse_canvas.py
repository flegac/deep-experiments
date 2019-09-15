import tkinter as tk

import cv2
from PIL import ImageTk, Image

from editor.hidden_scrollbar import HiddenScrollbar


# basic bersion :
# https://stackoverflow.com/questions/25787523/move-and-zoom-a-tkinter-canvas-with-mouse

# advanced version :
# https://stackoverflow.com/questions/41656176/tkinter-canvas-zoom-move-pan/48137257#48137257
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
        self.data = None
        self.image = None
        self.image_id = None
        self.zoom_factor = 1.

        # help
        self.text_id = self.canvas.create_text(2, 2, anchor='nw', text='Click and drag to move\nScroll to zoom')

        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda _: self.redraw_canvas)

        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>', self.move_to)
        # linux scroll
        self.canvas.bind('<Button-4>', self.zoom)  # wheel scroll up
        self.canvas.bind('<Button-5>', self.zoom)  # wheel scroll down
        # windows scroll
        self.canvas.bind('<MouseWheel>', self.zoom)

    def open(self, path: str):
        self.data = cv2.imread(path)
        self.data = cv2.cvtColor(self.data, cv2.COLOR_BGR2RGB)
        self.redraw_canvas()

    def move_from(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.redraw_canvas()

    def zoom(self, event):
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale *= self.ZOOM_SPEED
            self.zoom_factor *= self.ZOOM_SPEED
        if event.num == 4 or event.delta == 120:
            scale /= self.ZOOM_SPEED
            self.zoom_factor /= self.ZOOM_SPEED
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.redraw_canvas()

    def redraw_canvas(self):
        if self.image_id:
            self.canvas.delete(self.image_id)

        # extract data
        height, width = self.data.shape[:2]
        new_size = int(self.zoom_factor * width), int(self.zoom_factor * height)

        data = cv2.resize(self.data, new_size)

        self.image = ImageTk.PhotoImage(image=Image.fromarray(data))
        self.image_id = self.canvas.create_image(self.canvas.coords(self.text_id), anchor=tk.NW, image=self.image)
        self.canvas.lower(self.image_id)  # set it into background
        # self.canvas.configure(scrollregion=self.canvas.bbox("all"))


if __name__ == "__main__":
    root = tk.Tk()
    canvas = MouseCanvas(root)
    canvas.open('D:\\Datasets\\change\\20190802_export_s2_it1\\images\\nouakchott_1_s2_0.tif')

    root.mainloop()
