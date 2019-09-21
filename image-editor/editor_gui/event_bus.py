from dataclasses import dataclass, field

from rx.subject import Subject

PROJECT_OPEN_BUS = Subject()

FILE_OPEN_BUS = Subject()


@dataclass
class OpenFileEvent:
    editor_type: str = field(default=None)
    name: str = field(default=None)
    path: str = field(default=None)
