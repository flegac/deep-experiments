import math
from pathlib import Path

from cloud_runner.cluster.google_cluster import GoogleCluster
from cloud_runner.cluster.google_utils import cpu_config
from cloud_runner.script_runner import ScriptRunner

root = Path.cwd().parent.parent.parent.parent
ScriptRunner(
    creation_sleep_time=60,
    script_relative_path='my-mini-project/mini_project/script_local.py',
    config_relative_path='my-mini-project/mini_project/config.json',
    configs=[{
        'optimizer': i,
        'loss': i,
        'learning_rate': math.pow(10, -(i + 2))
    } for i in range(1)],
    to_deploy=[
        str(Path('my-mini-project').parent.parent),
        str(root / 'surili-lib'),
        str(root / 'stream-lib'),
    ]
).run_with(GoogleCluster(
    name='test-cluster',
    cluster_size=1,
    cluster_config=cpu_config()
))
