import abc
import subprocess
from typing import List, Union


class CloudCluster(abc.ABC):

    def __init__(self, cluster_size: int, remote_workspace: str):
        self._cluster_size = cluster_size
        self._remote_workspace = remote_workspace

    def create(self) -> subprocess.Popen:
        raise NotImplementedError()

    def delete(self) -> subprocess.Popen:
        raise NotImplementedError()

    def start(self, wait: bool = False) -> subprocess.Popen:
        raise NotImplementedError()

    def stop(self, wait: bool = True) -> subprocess.Popen:
        raise NotImplementedError()

    def ssh(self, commands: Union[str, List[str]], instance_id: int) -> subprocess.Popen:
        raise NotImplementedError()

    def push(self, local_path: str, remote_path: str, instance_id: int) -> subprocess.Popen:
        raise NotImplementedError()

    def pull(self, local_path: str, remote_path: str, instance_id: int) -> subprocess.Popen:
        raise NotImplementedError()

    def connection_command(self, instance_id: int) -> str:
        raise NotImplementedError()

    def cluster_size(self) -> int:
        return self._cluster_size

    def remote_workspace(self) -> str:
        return self._remote_workspace
