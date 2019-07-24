import shlex
import subprocess
from typing import List, Union


class CloudCluster(object):
    CREATE_COMMAND = 'gcloud compute instances create {instances} {config} --zone={zone}'
    DELETE_COMMAND = 'gcloud compute instances delete {instances} --zone={zone} -q'
    STOP_COMMAND = 'gcloud compute instances stop {instances} --zone={zone} {wait}'
    START_COMMAND = 'gcloud compute instances start {instances} --zone={zone} {wait}'
    SSH_COMMAND = "gcloud compute ssh --zone {zone} {instances} --command '{command}'"

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

    def create(self):
        shell(CloudCluster.CREATE_COMMAND.format(
            instances=' '.join(self.instances),
            config=' '.join(self.cluster_config),
            zone=self.zone
        )).wait()

    def start(self, wait: bool = False):
        try:
            shell(CloudCluster.START_COMMAND.format(
                instances=' '.join(self.instances),
                zone=self.zone,
                wait='--async' if wait else ''
            )).wait()
        except:
            self.create()

    def stop(self, wait: bool = True):
        shell(CloudCluster.STOP_COMMAND.format(
            instances=' '.join(self.instances),
            zone=self.zone,
            wait='--async' if wait else ''
        )).wait()

    def delete(self):
        shell(CloudCluster.DELETE_COMMAND.format(
            instances=' '.join(self.instances),
            zone=self.zone
        )).wait()

    def ssh(self, commands: Union[str, List[str]], instance_id: int = None):
        cmd = commands if isinstance(commands, str) else ' && '.join(commands)
        instances = ' '.join(self.instances) if instance_id is None else self.instances[instance_id]
        return shell(CloudCluster.SSH_COMMAND.format(
            instances=instances,
            zone=self.zone,
            command=cmd
        ))

    def push(self, local_path: str, remote_path: str, instance_id: int = None):
        cmd = 'gsutil -m cp -R {} {}'.format(local_path, remote_path)
        raise NotImplementedError()


def shell(cmd):
    print(cmd)
    # return subprocess.check_output(cmd, shell=True)

    return subprocess.Popen(shlex.split(cmd), shell=True)
