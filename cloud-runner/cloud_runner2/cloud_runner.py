import os
from typing import List, Generator, Dict

from cloud_runner2.cloud_cluster import CloudCluster
from surili_core.utils import wait_all
from surili_core.workspace import Workspace


class CloudRunner2(object):
    def __init__(self,
                 script_relative_path: str,
                 config_relative_path: str,
                 to_deploy: List[str],
                 config_generator: Generator[Dict, None, None],
                 ):
        self.script_relative_path = script_relative_path
        self.config_relative_path = config_relative_path
        self.to_deploy = to_deploy
        self.config_generator = config_generator
        self.ws: Workspace = None

    def run_with(self, cluster: CloudCluster):
        self.ws = Workspace.temporary('cloud_runner_').get_ws('workspace')

        archive_name = 'workspace.zip'
        archives = [self.create_local_workspace(_) for _ in range(cluster.size)]
        remote_workspace = '/tmp/workspace'
        remote_archive = '/'.join([remote_workspace, archive_name])

        try:
            # prepare all instances
            cluster.create().wait()
            cluster.ssh(commands=[
                'rm -rf {}'.format(remote_workspace),
                'mkdir {}'.format(remote_workspace),
            ]).wait()

            # deploy to all instances
            wait_all([
                cluster.push(
                    local_path=archive_path,
                    remote_path=remote_archive,
                    instance_id=_
                ) for _, archive_path in enumerate(archives)
            ])

            # run script on each instance
            cluster.ssh(commands=[
                'cd {}'.format(remote_workspace),
                'unzip {}'.format(archive_name),
                'rm {}'.format(archive_name),
                'export PYTHONPATH=${{PYTHONPATH}}:{}'.format(remote_workspace),
                'cd {}/{}'.format(remote_workspace, os.path.dirname(self.script_relative_path)),
                'python3 {}'.format(os.path.basename(self.script_relative_path))
            ]).wait()

            print('***** SSH COMMANDS *****')
            for _ in cluster.instances:
                print('\tgcloud beta compute ssh --zone "{}" "{}"'.format(cluster.zone, _))

        finally:
            self.ws.delete()
            for _ in archives:
                os.remove(_)

    def create_local_workspace(self, instance_id: int):
        ws = self.ws.get_ws(str(instance_id))
        for _ in self.to_deploy:
            ws.copy_from(_)
        dir_name, basename = os.path.split(self.config_relative_path)
        ws.get_ws(dir_name).create_file(basename, next(self.config_generator), force=True)

        return ws.archive(name='workspace')
