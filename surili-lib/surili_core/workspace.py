import json
import os
import pickle

from stream_lib.stream import stream


class Workspace:
    workspace = ''

    @staticmethod
    def from_path(path: str, auto_mkdir=True):
        return Workspace(os.path.join(Workspace.workspace, path), auto_mkdir)

    def __init__(self, path: str, auto_mkdir):
        self.path = path
        if os.path.splitext(path)[1] == '' and auto_mkdir:
            try:
                os.makedirs(self.path, exist_ok=True)
            except:
                pass

    def list_dir(self, root_path: str):
        return stream(os.listdir(root_path)).map(lambda x: os.path.join(root_path, x))

    def path_to(self, path):
        return os.path.join(self.path, path)

    def get_ws(self, path):
        return Workspace.from_path(self.path_to(path))

    def files(self):
        return stream(os.listdir(self.path)) \
            .map(lambda x: os.path.join(self.path, x))

    def touch(self, filename: str, content: dict):
        path = os.path.dirname(filename)
        if path != filename:
            self.get_ws(path)
        with open(self.path_to(filename), 'a') as _:
            os.utime(self.path_to(filename), None)
            if content:
                json.dump(content, _, indent=2, sort_keys=True)

    def save(self, name_function):
        if not callable(name_function):
            name = name_function
            name_function = lambda x: name

        def apply(data):
            path = self.path_to(name_function(data))
            with open(path, 'wb') as file:
                pickle.dump(data, file)
            return path

        return apply

    def load(self):
        def apply(path):
            path = os.path.join(self.path, path)
            with open(path, 'rb') as file:
                return pickle.load(file)

        return apply

    def __repr__(self) -> str:
        return '[FS: {}]'.format(self.path)
