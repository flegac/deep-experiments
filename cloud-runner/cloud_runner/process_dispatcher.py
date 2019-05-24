import os
from shutil import copyfile
from string import Template
from typing import List

import numpy as np

from cloud_runner.cloud import GCloud


class ProcessDispatcher(object):
    def __init__(self, vm_number: int, params: List[dict]):
        self._batches = np.array_split(params, vm_number)

    def batches(self):
        return self._batches


class InstanceWorkspace(object):
    class_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(class_path, 'resources/workspace_runner_template.py')) as _:
        workspace_template = Template(_.read())

    def __init__(self, config: dict, root_path: str, script_path: str, params: List[dict]):
        self.config = config
        self.path = os.path.join(root_path, 'instance_{}'.format(config['instance']))
        self.script_path = script_path
        self.params = params
        self.cloud = None

    def create_instance(self):
        try:
            self.cloud = GCloud.connect(**self.config)
            self.cloud.ssh_command('ls')
        except Exception as e:
            print(e)
            self.cloud = GCloud.create(**self.config)

    def generate(self):
        print('generate instance workspaces : {}'.format(os.path.basename(self.path)))
        os.makedirs(self.path, exist_ok=True)
        with open(os.path.join(self.path, 'runner.py'), 'w') as _:
            content = self.workspace_template.substitute(root_path=self.path)
            _.write(content)

        for i, x in enumerate(self.params):
            process = ProcessWorkspace(i, self.path, self.script_path)
            process.generate(x)

    def deploy(self):
        lib_path = os.path.abspath(os.path.join(__file__, '../..'))
        self.cloud.copy_upload(lib_path, '/tmp')
        self.cloud.copy_upload(self.path, '/tmp')
        self.cloud.ssh_command('sudo chmod +x /tmp/cloud-runner/cloud_runner/resources/deploy.sh')
        self.cloud.ssh_command('sudo /tmp/cloud-runner/cloud_runner/resources/deploy.sh')

    def run(self):
        basename = os.path.basename(self.path)
        self.cloud.ssh_command('cd /tmp/{} && python3 runner.py'.format(basename))


class ProcessWorkspace(object):
    class_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(class_path, 'resources/local_runner.py.tpl')) as _:
        local_template = Template(_.read())

    def __init__(self, id: int, root_path: str, script_path: str):
        self.path = os.path.join(root_path, 'workspace_{}'.format(id))
        self.script_path = script_path

    def generate(self, params: dict):
        print('workspace : {}'.format(str(params)))
        os.makedirs(self.path, exist_ok=True)

        copyfile(self.script_path, os.path.join(self.path, self.script_path))

        with open(os.path.join(self.path, 'runner.py'), 'w') as _:
            content = ProcessWorkspace.local_template.substitute(script_path=self.script_path, params=params)
            _.write(content)
