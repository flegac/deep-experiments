import imghdr
import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode, TreeItem
from typing import List

from editor_api.project import Project
from editor_gui.config import EDITOR_CONFIG
from editor_gui.event_bus import PROJECT_OPEN_BUS, IMAGE_OPEN_BUS, DATASET_OPEN_BUS, TEXT_OPEN_BUS
from editor_gui.utils.ui_utils import dir_selection, add_popup, build_menu


class ProjectBrowser(tk.LabelFrame):
    def __init__(self, master: tk.Widget):
        super().__init__(master, text="project")
        PROJECT_OPEN_BUS.subscribe(on_next=self.open_project)
        self.project: Project = None
        self.canvas = None

        # menu = build_menu(self, {
        #     'open': self.open_project,
        #     'add dataset': lambda: self.add_path(self.project.datasets),
        #     'add code': lambda: self.add_path(self.project.sources),
        # })
        # menu.pack(expand=True, fill=tk.BOTH, side=tk.TOP)

        button = tk.Button(self, text='open', command=self.open_project)
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add dataset', command=lambda: self.add_path(self.project.datasets))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add source', command=lambda: self.add_path(self.project.sources))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

    def add_path(self, target: List[str], path: str = None):
        path = path or dir_selection()
        if path == '':
            return
        target.append(path)
        self.project.save()
        self.canvas = self.redraw_explorer()

    def open_project(self, path: str = None):
        path = path or dir_selection()
        if path is None:
            return
        self.project = Project.from_path(path)
        self.project.save()
        EDITOR_CONFIG.config['default_project'] = self.project.workspace
        EDITOR_CONFIG.save_config()

        self.canvas = self.redraw_explorer()

    def redraw_explorer(self):
        if self.canvas is not None:
            self.canvas.destroy()

        sc = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1, width=200)
        sc.frame.pack(expand=True, fill="both", side=tk.BOTTOM)

        node = MyTreeNode(sc.canvas, None, ProjectTreeItem(self.project))
        node.expand()

        add_popup(self, build_menu(self, {
            'add dataset': lambda: self.add_path(self.project.datasets),
            'add source': lambda: self.add_path(self.project.sources),
        }))

        return sc.frame


class MyTreeNode(TreeNode):
    def select(self, event=None):
        TreeNode.select(self, event)
        if isinstance(self.item, ProjectTreeItem):
            return

        if isinstance(self.item, FileTreeItem):
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
