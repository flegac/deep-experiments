import imghdr
import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode

from editor_gui.events import PROJECT_OPEN_BUS, IMAGE_OPEN_BUS, DATASET_OPEN_BUS, TEXT_OPEN_BUS


class ProjectBrowser(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        super().__init__(master, text="project")
        PROJECT_OPEN_BUS.subscribe(on_next=self.open_project)

        self.sc = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1, width=200)
        self.sc.frame.pack(expand=True, fill="both", side=tk.LEFT)
        self.node = None

    def open_project(self, path: str):
        if self.node is not None:
            self.node.destroy()

        self.node = MyTreeNode(self.sc.canvas, None, FileTreeItem(path))
        self.node.expand()


class MyTreeNode(TreeNode):
    def select(self, event=None):
        TreeNode.select(self, event)
        path = str(self.item.path)
        print('self.item.GetText(): {!r}'.format(self.item.GetText()))
        print('self.item.path: "{}"'.format(path))
        name = os.path.basename(path)
        if os.path.isfile(path):
            if path.endswith('.csv'):
                DATASET_OPEN_BUS.on_next((name, path))
            elif imghdr.what(path) is not None:
                IMAGE_OPEN_BUS.on_next((name, path))
            elif path.endswith('.txt') or path.endswith('.json') or path.endswith('.py'):
                TEXT_OPEN_BUS.on_next((name, path))
            else:
                print('unsupported file format !')
