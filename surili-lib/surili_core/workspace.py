import json
import os
import pickle
import shutil
import tempfile
import time
import zipfile
from typing import Callable, Any

from stream_lib.stream import stream
from stream_lib.stream_api import Stream


class Workspace:
    workspace = ''

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.delete()

    @staticmethod
    def temporary(prefix: str = None, suffix: str = None, root_path=None):
        return Workspace.from_path(tempfile.mkdtemp(prefix=prefix, suffix=suffix, dir=root_path))

    @staticmethod
    def from_path(path: str):
        root_path = os.path.join(Workspace.workspace, path)
        return Workspace(root_path, root_path)

    def __init__(self, root_path: str, path: str):
        root_path = clean_path(root_path)
        path = clean_path(path)

        assert path.startswith(root_path), \
            'Workspace path must be in its root directory !'
        assert not os.path.exists(path) or os.path.isdir(path), \
            'Workspace must be a directory !'
        self._root_path = root_path
        self._current_path = path

        self.mkdir()

    def create_file(self, filename: str, content: dict = None, force=False):
        new_file = self.path_to(filename)
        if not force and os.path.exists(new_file):
            raise ValueError('File {} exists ! use force=True to force creation.'.format(new_file))

        with open(new_file, 'w') as _:
            os.utime(new_file, None)
            if content:
                json.dump(content, _, indent=2, sort_keys=True)
        return new_file

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
    def folders(self) -> 'Stream[Workspace]':
        return stream(os.listdir(self.path)) \
            .map(self.get_ws) \
            .filter(lambda _: os.path.isdir(_.path))

    @property
    def files(self) -> Stream[str]:
        return stream(os.listdir(self.path)) \
            .map(self.path_to) \
            .filter(os.path.isfile)

    def extract(self, archive_path: str):
        with zipfile.ZipFile(archive_path, 'r') as _:
            _.extractall(self.path)

    def archive(self, name: str = None):
        name = name or os.path.basename(self.path) + time.strftime("-%Y_%m_%d-%Hh%Mm%S")
        return shutil.make_archive(Workspace.temporary().path_to(name), 'zip', self.path)

    def copy_from(self, path: str):
        if os.path.isfile(path):
            shutil.copy(path, self.path_to(os.path.basename(path)))
        else:
            shutil.copytree(path, self.path_to(os.path.basename(path)))

    def delete(self):
        shutil.rmtree(self.path)

    def path_to(self, path: str):
        return clean_path(os.path.join(self.path, path))

    def get_ws(self, path: str):
        return Workspace(self._root_path, self.path_to(path))

    def __truediv__(self, path: str):
        return self.get_ws(path)

    def writer(self, name_provider: Callable[[Any], str]):
        def apply(data):
            name = name_provider if isinstance(name_provider, str) else name_provider(data)
            path = self.path_to(name)
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
