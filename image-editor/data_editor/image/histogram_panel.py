import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from data_toolbox.image.buffer_factory import ImageFactory
from data_toolbox.image.source.buffer_source import BufferSource


class HistogramPanel(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        tk.LabelFrame.__init__(self, master, text='visu')
        self.fig = None
        self.canvas = None
        self.fig = plt.Figure(figsize=(3, 3), dpi=100)
        self.ax = [
            self.fig.add_subplot(311),
            self.fig.add_subplot(312),
            self.fig.add_subplot(313)
        ]

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

    def update_data(self, source: BufferSource):
        data = source.get_data()

        if len(data.shape) == 2:
            return
        color = ('red', 'green', 'blue')

        for ax in self.ax:
            ax.clear()
        for i, col in enumerate(color):
            hist, bins = np.histogram(data[:, :, i], bins=256, range=None)
            hist = (hist - hist.min()) / hist.max()
            self.ax[i].plot(bins[:-1], hist, color=col, label=col)
            self.ax[i].legend()
            # self.ax[i].axis('off')
            self.ax[i].margins(0.01)
        self.fig.tight_layout()

        self.fig.canvas.draw()


if __name__ == '__main__':
    root = tk.Tk()
    editor = HistogramPanel(root)
    editor.update_data(ImageFactory.random)
    editor.pack()
    root.mainloop()
