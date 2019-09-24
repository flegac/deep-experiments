from dataclasses import dataclass, field

from rx.subject import Subject

OPEN_PROJECT_BUS = Subject()


@dataclass
class OpenProjectEvent:
    name: str = field(default=None)


OPEN_FILE_BUS = Subject()


@dataclass
class OpenFileEvent:
    editor_type: str = field(default=None)
    name: str = field(default=None)
    path: str = field(default=None)
