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
        self.fig = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = [
            self.fig.add_subplot(311),
            self.fig.add_subplot(312),
            self.fig.add_subplot(313)
        ]
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH)

    def update_data(self, data: np.ndarray):
        if len(data.shape) == 2:
            return
        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([data], [i], None, [256], [0, 256])
            self.ax[i].clear()
            self.ax[i].plot(histr, color=col)
        self.fig.canvas.draw()
