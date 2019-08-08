import math

from cloud_runner.script_runner import ScriptRunner
from cloud_runner.cluster.google_cluster import GoogleCluster
from cloud_runner.cluster.google_utils import cpu_config

ScriptRunner(
    creation_sleep_time=30,
    script_relative_path='my-mini-project/mini_project/script_local.py',
    config_relative_path='my-mini-project/mini_project/config.json',
    configs=[{
        'optimizer': i,
        'loss': i,
        'learning_rate': math.pow(10, -(i + 2))
    } for i in range(1)],
    to_deploy=[
        '../../my-mini-project',
        '../../../../surili-lib',
        '../../../../stream-lib',
    ]
).run_with(GoogleCluster(
    name='test-cluster',
    cluster_size=1,
    cluster_config=cpu_config()
))
