import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode


class FileBrowser(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, text="browser", width=150)

        sc = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1)
        sc.frame.pack(expand=True, fill="both", side=tk.LEFT)
        item = FileTreeItem(os.getcwd())
        node = TreeNode(sc.canvas, None, item)
        node.expand()
