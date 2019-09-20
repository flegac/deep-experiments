import tkinter as tk
from tkinter.scrolledtext import ScrolledText

root = tk.Tk(className=" Just another Text Editor")
textPad = ScrolledText(root, width=100, height=80, wrap=tk.WORD)
textPad.insert('1.0', 'fdsfdsfds')
textPad.pack()
root.mainloop()
