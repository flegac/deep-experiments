import os
import subprocess
from typing import List, Union

from cloud_runner.cluster.cloud_cluster import CloudCluster
from surili_core.utils import shell
from surili_core.workspace import Workspace


class LocalCluster(CloudCluster):

    def __init__(self, cluster_size: int, remote_workspace: str):
        super().__init__(cluster_size, remote_workspace)
        self.remote_ws = Workspace.from_path(remote_workspace)

    def create(self) -> subprocess.Popen:
        return shell('')

    def delete(self) -> subprocess.Popen:
        return shell('')

    def start(self, wait: bool = False) -> subprocess.Popen:
        return shell('')

    def stop(self, wait: bool = True) -> subprocess.Popen:
        return shell('')

    def ssh(self, commands: Union[str, List[str]], instance_id: int = None) -> subprocess.Popen:
        cmd = commands if isinstance(commands, str) else ' ; '.join(commands)
        return shell(cmd)

    def push(self, local_path: str, remote_path: str, instance_id: int = None) -> subprocess.Popen:
        if os.path.isdir(remote_path):
            raise ValueError('remote path must be a filename : {}'.format(remote_path))
        self.remote_ws.get_ws(remote_path).parent.copy_from(local_path)
        return shell('')

    def pull(self, local_path: str, remote_path: str, instance_id: int = None) -> subprocess.Popen:
        Workspace.from_path(local_path).copy_from(self.remote_ws.path_to(remote_path))
        return shell('')

    def connection_command(self, instance_id: int) -> str:
        return 'cd {}'.format(self.remote_ws.path_to(str(instance_id)))
