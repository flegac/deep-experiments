import os
from typing import List, Dict

from cloud_runner.cluster.cloud_cluster import CloudCluster
from surili_core.utils import wait_all
from surili_core.workspace import Workspace


class ScriptRunner(object):
    archive_name = 'workspace.zip'

    def __init__(self,
                 script_relative_path: str,
                 config_relative_path: str,
                 to_deploy: List[str],
                 configs: List[Dict],
                 ):
        self.script_relative_path = script_relative_path
        self.config_relative_path = config_relative_path
        self.to_deploy = to_deploy
        self.configs = configs

    def run_with(self, cluster: CloudCluster):
        if cluster.cluster_size() < len(self.configs):
            raise ValueError('Not enough instance to run each config, split your process !')
        remote_workspace = cluster.remote_workspace()
        remote_archive = '/'.join([remote_workspace, ScriptRunner.archive_name])

        runner_ws = Workspace.temporary('cloud_runner_').get_ws('workspace')
        try:
            # prepare all instances
            cluster.create().wait()

            wait_all([
                cluster.ssh(
                    commands=[
                        'rm -rf {}'.format(remote_workspace),
                        'mkdir {}'.format(remote_workspace),
                    ],
                    instance_id=_
                ) for _ in range(cluster.cluster_size())
            ])

            # push workspace archive file to each instance
            archives = [self.create_local_workspace(runner_ws, _) for _ in range(cluster.cluster_size())]
            wait_all([
                cluster.push(
                    local_path=archive_path,
                    remote_path=remote_archive,
                    instance_id=_
                ) for _, archive_path in enumerate(archives)
            ])
            for _ in archives:
                os.remove(_)

            # run script on each instance
            wait_all([
                cluster.ssh(
                    commands=[
                        'cd {}'.format(remote_workspace),
                        'unzip {}'.format(ScriptRunner.archive_name),
                        'rm {}'.format(ScriptRunner.archive_name),
                        'export PYTHONPATH=${{PYTHONPATH}}:{}'.format(remote_workspace),
                        'cd {}/{}'.format(remote_workspace, os.path.dirname(self.script_relative_path)),
                        'python3 {} >> out.log 2>> err.log'.format(os.path.basename(self.script_relative_path))
                    ],
                    instance_id=_
                ) for _ in range(cluster.cluster_size())
            ])

            print('***** SSH COMMANDS *****')
            for _ in range(cluster.cluster_size()):
                print(cluster.connection_command(_))

        finally:
            runner_ws.delete()

    def create_local_workspace(self, runner_ws: Workspace, instance_id: int):
        ws = runner_ws.get_ws(str(instance_id))
        for _ in self.to_deploy:
            ws.copy_from(_)

        dir_name, basename = os.path.split(self.config_relative_path)
        ws.get_ws(dir_name).create_file(basename, self.configs[instance_id], force=True)

        return ws.archive(name=os.path.splitext(ScriptRunner.archive_name)[0])
