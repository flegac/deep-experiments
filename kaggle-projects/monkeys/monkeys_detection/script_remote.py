from cloud_runner.cluster.google_cluster import GoogleCluster
from cloud_runner.cluster.google_utils import cpu_config
from cloud_runner.script_runner import ScriptRunner

configs = [
    {
        "input_shape": [128, 128, 3],
        "epochs": 2,
        "patience": 10,
        "workspace": "/tmp/project"

    }
]

ScriptRunner(
    script_relative_path='monkeys/monkeys_detection/script_local.py',
    config_relative_path='monkeys/monkeys_detection/config.json',
    configs=configs,
    to_deploy=[
        '../../monkeys',
        '../../../mydeep-lib',
        '../../../stream-lib',
        '../../../surili-lib',
        '../../../hyper-search'
    ],
    creation_sleep_time=0
).run_with(GoogleCluster(
    name='monkeys-cluster',
    cluster_size=1,
    cluster_config=cpu_config()  # gpu_config(GpuType.K80)
))
