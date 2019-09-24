from typing import Callable, Any

from editor_core.image.viewport import ViewportOperator


class ViewController(object):
    ZOOM_SPEED = 0.75
    EVENTS = [
        '<ButtonPress-1>',
        '<B1-Motion>',
        '<Button-4>',
        '<Button-5>',
        '<MouseWheel>',
        '<Key>'
    ]

    def __init__(self, canvas, on_update: Callable[[], Any]):
        self.canvas = canvas
        self.on_update = on_update

        self.viewport = ViewportOperator(self.view_size)
        self.mouse_x = None
        self.mouse_y = None

    def reset_view(self):
        self.viewport.zoom_factor = 1.
        self.viewport.x = 0
        self.viewport.y = 0

    def mouse_image_coords(self):
        z = self.viewport.zoom_factor
        root = self.canvas.master
        x_target = int((root.winfo_pointerx() - root.winfo_rootx()) / z)
        y_target = int((root.winfo_pointery() - root.winfo_rooty()) / z)
        return self.viewport.canvas_to_image_coords(x_target, y_target)

    def bindings(self):
        return {
            '<ButtonPress-1>': self.start_move,
            '<B1-Motion>': self.move,
            '<Button-4>': self.zoom,
            '<Button-5>': self.zoom,
            '<MouseWheel>': self.zoom
        }

    def unbind_canvas(self):
        if self.canvas is not None:
            for _ in self.EVENTS:
                self.canvas.unbind(_)
            self.canvas = None

    def view_size(self):
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
        self.on_update()

    def zoom(self, event):
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            self.viewport.zoom(self.ZOOM_SPEED)
        if event.num == 4 or event.delta == 120:
            self.viewport.zoom(1 / self.ZOOM_SPEED)
        self.on_update()
