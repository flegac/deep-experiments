from rx.subject import Subject

from editor_core.viewport import ViewportOperator


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

    def get_image_coords(self):
        # FIXME: scale & translate when image is too big (black borders)
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
