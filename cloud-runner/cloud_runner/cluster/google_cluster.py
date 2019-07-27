import subprocess
from typing import List, Union

from cloud_runner.cluster.cloud_cluster import CloudCluster
from surili_core.utils import shell


class GoogleCluster(CloudCluster):
    CREATE_COMMAND = 'gcloud compute instances create {instances} {config} --zone={zone}'
    DELETE_COMMAND = 'gcloud compute instances delete {instances} --zone={zone} -q'
    STOP_COMMAND = 'gcloud compute instances stop {instances} --zone={zone} {wait}'
    START_COMMAND = 'gcloud compute instances start {instances} --zone={zone} {wait}'
    SSH_COMMAND = 'gcloud compute ssh --zone {zone} {instances} --command "{command}"'
    PUSH_COMMAND = 'gcloud compute scp --recurse --zone {zone} "{local_path}" "{instance}:{remote_path}"'
    PULL_COMMAND = 'gcloud compute scp --recurse --zone {zone} "{instance}:{remote_path}" "{local_path}"'
    CONNECT_COMMAND = 'gcloud beta compute ssh --zone "{zone}" "{instance}"'

    def __init__(self,
                 name: str,
                 cluster_size: int,
                 zone: str = 'europe-west1-b',
                 cluster_config: List[str] = None,
                 remote_workspace: str = '/tmp/workspace'
                 ):
        super().__init__(cluster_size, remote_workspace)
        self.cluster_config = cluster_config or []
        self.zone = zone
        self.name = name
        self.instances = ['{}-{}'.format(name, i) for i in range(cluster_size)]
        self.instances_string = ' '.join(self.instances)

    def remote_workspace(self):
        return self._remote_workspace

    def create(self) -> subprocess.Popen:
        return shell(GoogleCluster.CREATE_COMMAND.format(
            instances=self.instances_string,
            config=' '.join(self.cluster_config),
            zone=self.zone
        ))

    def delete(self) -> subprocess.Popen:
        return shell(GoogleCluster.DELETE_COMMAND.format(
            instances=self.instances_string,
            zone=self.zone
        ))

    def start(self, wait: bool = False) -> subprocess.Popen:
        return shell(GoogleCluster.START_COMMAND.format(
            instances=self.instances_string,
            zone=self.zone,
            wait='--async' if wait else ''
        ))

    def stop(self, wait: bool = True) -> subprocess.Popen:
        return shell(GoogleCluster.STOP_COMMAND.format(
            instances=self.instances_string,
            zone=self.zone,
            wait='--async' if wait else ''
        ))

    def ssh(self, commands: Union[str, List[str]], instance_id: int) -> subprocess.Popen:
        cmd = commands if isinstance(commands, str) else ' ; '.join(commands)
        return shell(GoogleCluster.SSH_COMMAND.format(
            instances=self.instances[instance_id],
            zone=self.zone,
            command=cmd
        ))

    def push(self, local_path: str, remote_path: str, instance_id: int) -> subprocess.Popen:
        cmd = GoogleCluster.PUSH_COMMAND.format(
            zone=self.zone,
            instance=self.instances[instance_id],
            local_path=local_path,
            remote_path=remote_path)
        return shell(cmd)

    def pull(self, local_path: str, remote_path: str, instance_id: int) -> subprocess.Popen:
        # os.makedirs(local_path, exist_ok=True)

        cmd = GoogleCluster.PULL_COMMAND.format(
            zone=self.zone,
            instance=self.instances[instance_id],
            local_path=local_path,
            remote_path=remote_path)
        return shell(cmd)

    def connection_command(self, instance_id: int) -> str:
        return GoogleCluster.CONNECT_COMMAND.format(zone=self.zone, instance=self.instances[instance_id])

    def _instance_string(self, instance_id: int):
        return self.instances[instance_id] if instance_id else self.instances_string
