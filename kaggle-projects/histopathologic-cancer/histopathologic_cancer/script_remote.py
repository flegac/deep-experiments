from cloud_runner.cluster.google_cluster import GoogleCluster
from cloud_runner.cluster.google_utils import gpu_config, GpuType
from cloud_runner.script_runner import ScriptRunner

configs = [
    {
        'input_shape': [96, 96, 3],
        'epochs': 100,
        'patience': 10
    }
]

ScriptRunner(
    script_relative_path='histopathologic-cancer/histopathologic_cancer/script_densenet_121_augmentation_CLR.py',
    config_relative_path='histopathologic-cancer/histopathologic_cancer/config.json',
    configs=configs,
    to_deploy=[
        '../../histopathologic-cancer',
        '../../../mydeep-lib',
        '../../../stream-lib',
        '../../../surili-lib',
        '../../../hyper-search'
    ]
).run_with(GoogleCluster(
    name='test-cluster',
    cluster_size=1,
    cluster_config=gpu_config(GpuType.K80)
))
