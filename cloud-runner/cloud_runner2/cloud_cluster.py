import shlex
import subprocess
from typing import List, Union


class CloudCluster(object):
    CREATE_COMMAND = 'gcloud compute instances create {instances} {config} --zone={zone}'
    DELETE_COMMAND = 'gcloud compute instances delete {instances} --zone={zone} -q'
    STOP_COMMAND = 'gcloud compute instances stop {instances} --zone={zone} {wait}'
    START_COMMAND = 'gcloud compute instances start {instances} --zone={zone} {wait}'
    SSH_COMMAND = "gcloud compute ssh --zone {zone} {instances} --command '{command}'"
    PUSH_COMMAND = "gcloud compute scp --recurse --zone {zone} '{local_path}' '{instance}:{remote_path}'"
    PULL_COMMAND = "gcloud compute scp --recurse --zone {zone} '{instance}:{remote_path}' '{local_path}'"

    def __init__(self,
                 name: str,
                 cluster_size: int,
                 zone: str = 'europe-west1-b',
                 cluster_config: List[str] = None,
                 ):
        self.cluster_config = cluster_config or []
        self.zone = zone
        self.name = name
        self.size = cluster_size
        self.instances = ['{}-{}'.format(name, i) for i in range(cluster_size)]
        self.instances_string = ' '.join(self.instances)

    def create(self):
        shell(CloudCluster.CREATE_COMMAND.format(
            instances=self.instances_string,
            config=' '.join(self.cluster_config),
            zone=self.zone
        )).wait()

    def start(self, wait: bool = False):
        try:
            shell(CloudCluster.START_COMMAND.format(
                instances=self.instances_string,
                zone=self.zone,
                wait='--async' if wait else ''
            )).wait()
        except:
            self.create()

    def stop(self, wait: bool = True):
        shell(CloudCluster.STOP_COMMAND.format(
            instances=self.instances_string,
            zone=self.zone,
            wait='--async' if wait else ''
        )).wait()

    def delete(self):
        shell(CloudCluster.DELETE_COMMAND.format(
            instances=self.instances_string,
            zone=self.zone
        )).wait()

    def ssh(self, commands: Union[str, List[str]], instance_id: int = None) -> subprocess.Popen:
        cmd = commands if isinstance(commands, str) else ' && '.join(commands)
        return shell(CloudCluster.SSH_COMMAND.format(
            instances=self._instance_string(instance_id),
            zone=self.zone,
            command=cmd
        ))

    def push(self, local_path: str, remote_path: str, instance_id: int = None) -> subprocess.Popen:
        cmd = CloudCluster.PUSH_COMMAND.format(
            zone=self.zone,
            instances=self._instance_string(instance_id),
            local_path=local_path,
            remote_path=remote_path)
        return shell(cmd)

    def pull(self, local_path: str, remote_path: str, instance_id: int = None) -> subprocess.Popen:
        # os.makedirs(local_path, exist_ok=True)

        cmd = CloudCluster.PULL_COMMAND.format(
            zone=self.zone,
            instances=self._instance_string(instance_id),
            local_path=local_path,
            remote_path=remote_path)
        return shell(cmd)

    def _instance_string(self, instance_id: int):
        return self.instances[instance_id] if instance_id else self.instances_string


def shell(cmd) -> subprocess.Popen:
    print(cmd)
    # return subprocess.check_output(cmd, shell=True)

    return subprocess.Popen(shlex.split(cmd), shell=True)
