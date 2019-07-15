import json
import os
import pickle
import shutil
from typing import List

from stream_lib.stream import stream
from stream_lib.stream_api import Stream


class Workspace:
    workspace = ''

    @staticmethod
    def from_path(path: str):
        root_path = os.path.join(Workspace.workspace, path)
        return Workspace(root_path, root_path)

    def __init__(self, root_path: str, path: str):
        root_path = clean_path(root_path)
        path = clean_path(path)

        assert path.startswith(root_path), \
            'Workspace path must be in its root directory'
        assert not os.path.exists(path) or os.path.isdir(path), \
            'Workspace must be a directory'

        self._root_path = root_path
        self._current_path = path

        self.mkdir()

    def create_file(self, filename: str, content: dict = None, force=False):
        new_file = self.path_to(filename)
        if not force and os.path.exists(new_file):
            raise ValueError('File {} exists ! use no_overwrite=False to force creation.'.format(new_file))

        with open(new_file, 'w') as _:
            os.utime(new_file, None)
            if content:
                json.dump(content, _, indent=2, sort_keys=True)

    def mkdir(self) -> 'Workspace':
        try:
            os.makedirs(self.path, exist_ok=True)
        except:
            pass
        return self

    @property
    def root(self) -> 'Workspace':
        return Workspace.from_path(self._root_path)

    @property
    def path(self) -> str:
        return self._current_path

    @property
    def parent(self) -> 'Workspace':
        return self.get_ws('..')

    @property
    def folders(self) -> 'List[Workspace]':
        return [
            self.get_ws(_)
            for _ in os.listdir(self.path)
            if os.path.isdir(self.path_to(_))
        ]

    @property
    def files(self) -> Stream[str]:
        return stream(os.listdir(self.path)) \
            .map(self.path_to) \
            .filter(os.path.isfile)

    def delete(self):
        shutil.rmtree(self.path)

    def path_to(self, path):
        return clean_path(os.path.join(self.path, path))

    def get_ws(self, path):
        return Workspace(self._root_path, self.path_to(path))

    def writer(self, name_function):
        if not callable(name_function):
            name = name_function
            name_function = lambda x: name

        def apply(data):
            path = self.path_to(name_function(data))
            with open(path, 'wb') as file:
                pickle.dump(data, file)
            return path

        return apply

    def reader(self):
        def apply(path):
            path = os.path.join(self.path, path)
            with open(path, 'rb') as file:
                return pickle.load(file)

        return apply

    def __repr__(self) -> str:
        return '[WS: {}]'.format(self.path)


def clean_path(path: str):
    return os.path.abspath(path)
