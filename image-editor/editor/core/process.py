from typing import Callable, Any

from editor.core.data import DataSource

ProcessUpdater = Callable[[float], Any]
DataProcess = Callable[[ProcessUpdater], None]
DataProcessFactory = Callable[[DataSource], DataProcess]
