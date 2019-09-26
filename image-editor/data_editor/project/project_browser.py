import os
import tkinter as tk
from idlelib.tree import ScrolledCanvas, FileTreeItem, TreeNode, TreeItem
from typing import List, Any, Callable

from rx.subject import Subject

from data_editor.editor_config import EditorManager
from data_editor.project.source_browser import SourceBrowser
from data_editor.project_config import ProjectConfig, ProjectManager
from data_editor.utils.file_select import ask_open_project, ask_dir_selection
from data_editor.utils.source_loader import load_source


class ProjectBrowser(tk.LabelFrame):
    def __init__(self, master: tk.Widget, manager: ProjectManager, on_open: Callable[[str], Any]):
        super().__init__(master, text="project")
        self.update_bus = Subject()
        self.update_bus.subscribe(on_next=self.open_project)

        self.manager = manager

        self.project: ProjectConfig = None

        button = tk.Button(self, text='open', command=lambda: self.open_project(ask_open_project()))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add dataset', command=lambda: self.add_path(self.project.datasets))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        button = tk.Button(self, text='add source', command=lambda: self.add_path(self.project.sources))
        button.pack(expand=False, fill=tk.X, side=tk.TOP)

        self.canvas = ScrolledCanvas(self, bg="white", highlightthickness=0, takefocus=1, width=250)

        def zoom(event):
            # Respond to Linux (event.num) or Windows (event.delta) wheel event
            if event.num == 5 or event.delta == -120:
                self.canvas.canvas.yview_scroll(1, "unit")
            if event.num == 4 or event.delta == 120:
                self.canvas.canvas.yview_scroll(-1, "unit")

        self.canvas.canvas.bind('<Button-4>', zoom)
        self.canvas.canvas.bind('<Button-5>', zoom)
        self.canvas.canvas.bind('<MouseWheel>', zoom)

        self.canvas.frame.pack(expand=False, fill=tk.X, side=tk.TOP)

        self.source_browser = SourceBrowser(self, on_open)
        self.source_browser.pack(expand=False, fill=tk.X, side=tk.TOP)

        self.request_update(manager.config.project)

    def add_path(self, target: List[str], path: str = None):
        if path is None:
            path = ask_dir_selection()
        if path == '':
            print('could not open project :' + str(path))
            return
        target.append(path)
        self.redraw_explorer()
        self.manager.save(self.project)

    def open_project(self, path: str = None):
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

    def request_update(self, project_name: str):
        self.update_bus.on_next(project_name)


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


if __name__ == '__main__':
    root = tk.Tk()
    widget = ProjectBrowser(root, ProjectManager(), lambda _: print(_))
    widget.pack(fill='both', expand=True)
    root.mainloop()
