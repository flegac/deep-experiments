import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode

from editor_gui.config import EDITOR_CONFIG
from editor_gui.utils.frame_manager import FrameManager


class FileBrowser(tk.LabelFrame):
    def __init__(self, master, editor: FrameManager):
        super().__init__(master, text="browser")
        self.editor = editor

        self.sc = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1, width=200)
        self.sc.frame.pack(expand=True, fill="both", side=tk.LEFT)
        self.node = None
        if EDITOR_CONFIG.config_path_is_valid('directory_browser_path'):
            self.open(EDITOR_CONFIG.config.get('directory_browser_path'))

    def open(self, path: str):
        editor = self.editor

        class MyTreeNode(TreeNode):
            def select(self, event=None):
                TreeNode.select(self, event)
                print('select called')
                print('self.item.GetText(): {!r}'.format(self.item.GetText()))
                print('self.item.path: "{}"'.format(self.item.path))
                name, _ = os.path.splitext(os.path.basename(self.item.path))
                if os.path.isfile(self.item.path):
                    editor.create(name, [self.item.path])

        if self.node is not None:
            self.node.destroy()

        self.node = MyTreeNode(self.sc.canvas, None, FileTreeItem(path))
        self.node.expand()
