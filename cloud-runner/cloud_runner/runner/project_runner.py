import abc


class ProjectRunner(abc.ABC):
    def run(self):
        raise NotImplementedError()
