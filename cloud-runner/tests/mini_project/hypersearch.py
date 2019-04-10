from cloud_runner.cloud import GCloud
from cloud_runner.runner.cloud_runner import CloudRunner

import math

project_id = GCloud.get_project_id('my-project-name')
cloud = {
    'user': 'my-username',
    'zone': 'europe-west1-b',
    'project_id': project_id,
    'config_path': 'vm.yaml'
}


def params_provider():
    for i in range(10):
        yield {
            'optimizer': i,
            'loss': i,
            'learning_rate': math.pow(10, -(i + 2)),
        }


CloudRunner(
    instance_prefix='toto',
    cloud_config=cloud,
    nb_vms=2,
    vm_path='vm.yaml',
    script_path='training_script.py',
    params_provider=params_provider
).run()
