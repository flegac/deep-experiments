import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode, TreeItem
from typing import List

from editor_gui.event_bus import OPEN_PROJECT_BUS, OPEN_FILE_BUS, OpenFileEvent
from editor_gui.file_select import ask_open_project, ask_dir_selection
from editor_core.config.editor import EditorManager
from editor_core.config.project import Project, ProjectManager


class ProjectBrowser(tk.LabelFrame):
    def __init__(self, master: tk.Widget, manager: ProjectManager):
        super().__init__(master, text="project")
        self.manager = manager
        OPEN_PROJECT_BUS.subscribe(on_next=self.open_project)
        self.project: Project = None
        self.canvas = None

        button = tk.Button(self, text='open', command=lambda: self.open_project(ask_open_project(self.manager.config)))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add dataset', command=lambda: self.add_path(self.project.datasets))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add source', command=lambda: self.add_path(self.project.sources))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)
        OPEN_PROJECT_BUS.on_next(manager.config.project)

    def add_path(self, target: List[str], path: str = None):
        if path is None:
            path = ask_dir_selection(self.manager.config)
        if path == '':
            print('could not open project :' + str(path))
            return
        target.append(path)
        self.canvas = self.redraw_explorer()
        self.manager.save(self.project)

    def open_project(self, path: str = None):
        self.project = self.manager.load(path)
        self.manager.save(self.project)
        self.manager.config.project = self.project.name
        EditorManager.save(self.manager.config)
        self.canvas = self.redraw_explorer()

    def redraw_explorer(self):
        if self.canvas is not None:
            self.canvas.destroy()

        sc = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1, width=200)
        sc.frame.pack(expand=True, fill="both", side=tk.BOTTOM)

        node = MyTreeNode(sc.canvas, None, ProjectTreeItem(self.project))
        node.expand()

        return sc.frame


class MyTreeNode(TreeNode):
    def select(self, event=None):
        TreeNode.select(self, event)
        if isinstance(self.item, ProjectTreeItem):
            return

        if isinstance(self.item, FileTreeItem):
            path = str(self.item.path)
            OPEN_FILE_BUS.on_next(OpenFileEvent(path=path))


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
    def __init__(self, project: Project):
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

        return [
            FileTreeItem(self.project.workspace),
            MultiRootFileTreeItem('datasets', self.project.datasets),
            MultiRootFileTreeItem('sources', self.project.sources),
        ]
