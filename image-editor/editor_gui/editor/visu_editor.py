import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VisuEditor(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='visu')
        self.fig = None
        self.canvas = None
        self.fig = plt.Figure(figsize=(4, 3), dpi=100)
        self.ax = [
            self.fig.add_subplot(311),
            self.fig.add_subplot(312),
            self.fig.add_subplot(313)
        ]

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

        self.text = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text)
        self.label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_data(self, name: str, data: np.ndarray):

        self.text.set('{} {}x{}'.format(name, data.shape[1], data.shape[0]))

        if len(data.shape) == 2:
            return
        color = ('red', 'green', 'blue')

        for ax in self.ax:
            ax.clear()
        for i, col in enumerate(color):
            # histr = cv2.calcHist([data], [i], None, [256], [0, 256])
            hist, bins = np.histogram(data[:, :, i], bins=256, range=None)
            # histr = (histr - histr.min()) / histr.max()
            self.ax[i].plot(bins[:-1], hist, color=col, label=col)
            self.ax[i].legend()
            self.ax[i].axis('off')
            self.ax[i].margins(0.01)
        self.fig.tight_layout()

        self.fig.canvas.draw()
