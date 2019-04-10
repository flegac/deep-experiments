from typing import List

from cloud_runner.process_dispatcher import ProcessDispatcher, InstanceWorkspace
from cloud_runner.runner.project_runner import ProjectRunner


class CloudRunner(ProjectRunner):

    def __init__(self,
                 cloud_config: dict,
                 nb_vms: int,
                 vm_path: str,
                 script_path: str,
                 params_provider,
                 workspace: str = 'workspaces',
                 instance_prefix: str = 'cloud-runner'):
        self.instance_prefix = instance_prefix
        self.nb_vms = nb_vms
        self.cloud_config = cloud_config
        self.workspace = workspace
        self.vm_path = vm_path
        self.script_path = script_path
        self.params_provider = params_provider

    def _create_instance_workspace(self, name: str, params: List[dict]):
        config = self.cloud_config.copy()
        config['instance'] = '{}-{}'.format(self.instance_prefix, name)
        return InstanceWorkspace(config, self.workspace, self.script_path, params)

    def run(self):
        processes = ProcessDispatcher(self.nb_vms, list(self.params_provider()))

        workspaces = [self._create_instance_workspace(str(i), params)
                      for i, params in enumerate(processes.batches())]

        for _ in workspaces:
            _.generate()
        for _ in workspaces:
            _.create_instance()
        for _ in workspaces:
            _.deploy()
        for _ in workspaces:
            _.run()

    def log(self, message: str):
        print(message)
