import imghdr
import os

from data_toolbox.buffer.buffer_factory import ImageFactory
from data_toolbox.table.table_source import TableSource


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
