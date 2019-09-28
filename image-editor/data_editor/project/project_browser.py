import imghdr
import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode, TreeItem
from tkinter import simpledialog
from typing import List, Any, Callable

from data_editor.editor_config import EditorManager
from data_editor.project.source_browser import SourceBrowser
from data_editor.project_config import ProjectConfig, ProjectManager
from data_editor.utils.file_select import ask_open_project, ask_dir_selection
from data_toolbox.image.buffer_factory import ImageFactory
from data_toolbox.table.table_source import TableSource


class ProjectBrowser(tk.LabelFrame):
    def __init__(self, master: tk.Widget, width: int):
        super().__init__(master, text="project")
        self.project: ProjectConfig = None

        button = tk.Button(self, text='open', command=lambda: self.open_project(ask_open_project()))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add dataset', command=lambda: self.add_path(self.project.datasets))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add source', command=lambda: self.add_path(self.project.sources))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        self.canvas = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1, width=width)
        self.canvas.frame.pack(expand=False, fill=tk.X, side=tk.TOP)

        self.source_browser = SourceBrowser(self)
        self.source_browser.pack(expand=False, fill=tk.X, side=tk.TOP)

        def zoom(event):
            # Respond to Linux (event.num) or Windows (event.delta) wheel event
            if event.num == 5 or event.delta == -120:
                self.canvas.canvas.yview_scroll(1, "unit")
            if event.num == 4 or event.delta == 120:
                self.canvas.canvas.yview_scroll(-1, "unit")

        self.canvas.canvas.bind('<Button-4>', zoom)
        self.canvas.canvas.bind('<Button-5>', zoom)
        self.canvas.canvas.bind('<MouseWheel>', zoom)

        self.manager = ProjectManager()
        self.open_project(self.manager.config.project)

    def subscribe(self, on_next=Callable[[Any], None]):
        self.source_browser.subscribe(on_next)

    def add_path(self, target: List[str], path: str = None):
        if path is None:
            path = ask_dir_selection()
        if path == '':
            print('could not open project :' + str(path))
            return
        target.append(path)
        self.redraw_explorer()
        self.manager.save(self.project)

    def create_project(self):
        name = simpledialog.askstring("Input", "Project Name",
                                      parent=self)
        workspace = os.path.join(self.manager.config.root_path, name)
        os.makedirs(workspace, exist_ok=True)
        self.project = ProjectConfig(name=name, workspace=workspace)
        self.manager.save(self.project)
        self.manager.config.project = self.project.name
        EditorManager.save(self.manager.config)
        self.redraw_explorer()

    def open_project(self, path: str = None):
        if path is None:
            return
        self.project = self.manager.load(path)
        self.manager.save(self.project)
        self.manager.config.project = self.project.name
        EditorManager.save(self.manager.config)
        self.redraw_explorer()

    def redraw_explorer(self):
        node = MyTreeNodeFactory.new_class(lambda _: self.source_browser.add_source(load_source(_)))(
            self.canvas.canvas,
            None,
            ProjectTreeItem(self.project)
        )
        node.expand()


class MyTreeNodeFactory(object):
    @staticmethod
    def new_class(on_open: Callable[[str], Any]):
        class MyTreeNode(TreeNode):
            def select(self, event=None):
                TreeNode.select(self, event)
                if isinstance(self.item, ProjectTreeItem):
                    return

                if isinstance(self.item, FileTreeItem):
                    path = str(self.item.path)
                    on_open(path)

        return MyTreeNode


class MultiRootFileTreeItem(TreeItem):
    def __init__(self, name: str, paths: List[str]):
        super().__init__()
        self.name = name
        self.paths = paths

    def GetText(self):
        return self.name

    def IsEditable(self):
        return False

    def SetText(self, text):
        newpath = os.path.dirname(self.path)
        newpath = os.path.join(newpath, text)
        if os.path.dirname(newpath) != os.path.dirname(self.path):
            return
        try:
            os.rename(self.path, newpath)
            self.path = newpath
        except OSError:
            pass

    def GetIconName(self):
        pass

    def IsExpandable(self):
        return True

    def GetSubList(self):
        paths = self.paths
        paths.sort(key=os.path.normcase)
        sublist = [
            FileTreeItem(_) for _ in paths
        ]
        return sublist


class ProjectTreeItem(TreeItem):
    def __init__(self, project: ProjectConfig):
        super().__init__()
        self.project = project

    def GetText(self):
        return self.project.name

    def IsEditable(self):
        return False

    def SetText(self, text):
        newpath = os.path.dirname(self.path)
        newpath = os.path.join(newpath, text)
        if os.path.dirname(newpath) != os.path.dirname(self.path):
            return
        try:
            os.rename(self.path, newpath)
            self.path = newpath
        except OSError:
            pass

    def GetIconName(self):
        pass

    def IsExpandable(self):
        return True

    def GetSubList(self):
        datasets = self.project.datasets
        datasets.sort(key=os.path.normcase)
        sources = self.project.sources
        sources.sort(key=os.path.normcase)

        children = [
            FileTreeItem(self.project.workspace),
            MultiRootFileTreeItem('datasets', self.project.datasets),
            MultiRootFileTreeItem('sources', self.project.sources),
        ]

        return children


def load_source(path: str):
    if os.path.isdir(path):
        return
    if path.endswith('.csv'):
        return TableSource().load(path)
    elif imghdr.what(path) is not None:
        return ImageFactory.from_rgb(path)
    elif path.endswith('.txt') or path.endswith('.json') or path.endswith('.py'):
        # TODO create TextSource
        return path
    else:
        raise ValueError('unsupported file format !')


if __name__ == '__main__':
    root = tk.Tk()
    widget = ProjectBrowser(root, width=200)
    widget.pack(fill='both', expand=True)
    root.mainloop()
