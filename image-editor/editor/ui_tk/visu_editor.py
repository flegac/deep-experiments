import tkinter as tk

import cv2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class VisuEditor(tk.LabelFrame):
    def __init__(self, master):
        tk.LabelFrame.__init__(self, master, text='visu')
        self.fig = None
        self.canvas = None
        self.fig = plt.Figure(figsize=(3, 2), dpi=100)
        self.ax = [
            self.fig.add_subplot(111),
            # self.fig.add_subplot(312),
            # self.fig.add_subplot(313)
        ]

        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)

        self.text = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.text)
        self.label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_data(self, data: np.ndarray):
        self.text.set('{}x{}'.format(data.shape[1], data.shape[0]))

        if len(data.shape) == 2:
            return
        color = ('red', 'green', 'blue')
        self.ax[0].clear()

        for i, col in enumerate(color):
            histr = cv2.calcHist([data], [i], None, [256], [0, 256])
            self.ax[0].plot(np.arange(256), histr, color=col, label=col)

        self.ax[0].legend()
        self.ax[0].axis('off')
        self.ax[0].margins(0.01)
        self.fig.tight_layout()

        self.fig.canvas.draw()
