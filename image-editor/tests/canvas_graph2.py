import time
import tkinter as tk
from typing import List


class Vertex(object):
    def __init__(self, name: str, x: int, y: int):
        self.name = name
        self.x = x
        self.y = y
        self.size = 10
        self.edges: List[Vertex] = []
        self.fid = None

    def draw(self, w):
        self.fid = w.create_rectangle(
            self.x - self.size,
            self.y - self.size,
            self.x + self.size,
            self.y + self.size,
            fill="blue")
        return w.create_text(self.x, self.y, text=self.name, tags="DnD")


class Graph(object):
    def __init__(self):
        self.vertices: List[Vertex] = []

    def add(self, vertex: Vertex):
        self.vertices.append(vertex)

    def link(self, i, j):
        self.vertices[i].edges.append(self.vertices[j])

    def redraw(self, w):
        widgets = []
        for v1 in self.vertices:
            for v2 in v1.edges:
                widgets.append(w.create_line(
                    v1.x, v1.y,
                    v2.x, v2.y,
                    fill="red",
                    dash=(4, 2)
                ))

        for v in self.vertices:
            widgets.append(
                v.draw(w)
            )
        return widgets


class CanvasDnD(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.defaultcolor = 'black'
        self.master = master
        self.loc = self.dragged = 0

        canvas = tk.Canvas(self, width=600, height=400,
                           relief=tk.RIDGE, background="white", borderwidth=1)

        canvas.pack(expand=1, fill=tk.BOTH)
        canvas.tag_bind("DnD", "<ButtonPress-1>", self.down)
        canvas.tag_bind("DnD", "<ButtonRelease-1>", self.chkup)
        canvas.tag_bind("DnD", "<Enter>", self.enter)
        canvas.tag_bind("DnD", "<Leave>", self.leave)
        self.canvas = canvas

        self.widgets = []
        self.draw_callback = None

    def down(self, event):
        self.loc = 1
        self.dragged = 0
        event.widget.bind("<Motion>", self.motion)

    def motion(self, event):
        self.master.config(cursor="exchange")
        cnv = event.widget
        cnv.itemconfigure(tk.CURRENT, fill="blue")
        x, y = cnv.canvasx(event.x), cnv.canvasy(event.y)
        got = event.widget.coords(tk.CURRENT, x, y)

    def leave(self, event):
        self.loc = 0

    def enter(self, event):
        self.loc = 1
        if self.dragged == event.time:
            self.up(event)

    def chkup(self, event):
        event.widget.unbind("<Motion>")
        self.master.config(cursor="")
        self.target = event.widget.find_withtag(tk.CURRENT)
        event.widget.itemconfigure(tk.CURRENT, fill=self.defaultcolor)
        if self.loc:  # is button released in same widget as pressed?
            self.up(event)
        else:
            self.dragged = event.time
        self._redraw()

    def up(self, event):
        event.widget.unbind("<Motion>")
        if (self.target == event.widget.find_withtag(tk.CURRENT)):
            pass
        else:
            event.widget.itemconfigure(tk.CURRENT, fill="blue")
            self.master.update()
            time.sleep(.1)

    def _redraw(self):
        if self.draw_callback is not None:
            self.canvas.delete('all')
            self.widgets = self.draw_callback(self.canvas)


def main2():
    root = tk.Tk()
    root.title("Drag-N-Drop Demo")
    canvas = CanvasDnD(root)
    canvas.pack()

    graph = Graph()
    graph.add(Vertex('A', 100, 100))
    graph.add(Vertex('B', 200, 100))
    graph.add(Vertex('C', 100, 200))
    graph.add(Vertex('D', 150, 150))
    graph.link(0, 1)
    graph.link(0, 2)
    graph.link(1, 3)

    canvas.draw_callback = graph.redraw

    graph.redraw(canvas.canvas)

    root.mainloop()


if __name__ == '__main__':
    main2()
