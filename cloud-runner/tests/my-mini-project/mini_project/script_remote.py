import math

from cloud_runner2.cloud_cluster import CloudCluster
from cloud_runner2.cloud_runner import CloudRunner2
from cloud_runner2.cluster_utils import cpu_config


def params_provider():
    for i in range(10):
        yield {
            'optimizer': i,
            'loss': i,
            'learning_rate': math.pow(10, -(i + 2)),
        }


cluster = CloudCluster(
    name='test-cluster',
    cluster_size=1,
    cluster_config=cpu_config()
)

CloudRunner2(
    script_relative_path='mini_project/script_local.py',
    config_relative_path='mini_project/config.json',
    config_generator=params_provider(),
    to_deploy=[
        '../mini_project',
        '../mini_lib'
    ]
).run_with(cluster)
