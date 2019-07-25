from cloud_runner2.cloud_cluster import CloudCluster
from cloud_runner2.cloud_runner import CloudRunner2
from cloud_runner2.cluster_utils import cpu_config
from surili_core.workspace import Workspace

cluster = CloudCluster(
    name='test-cluster',
    cluster_size=1,
    cluster_config=cpu_config()
)


def my_generator():
    yield {
        'a': 'aaaaa',
        'b': 'bbbbb'
    }


def test_start():
    root_ws = Workspace.temporary()
    ws = [root_ws.get_ws('project_{}'.format(_)) for _ in range(3)]
    for _ in ws:
        _.create_file('xxx.json', {
            'p1': 'toto',
            'p2': 'tata'
        })
        _.get_ws('conf').create_file('config.json', {
            'p1': 'toto',
            'p2': 'tata'
        })

    with open(ws[0].path_to('script_local.py'), 'w') as _:
        _.writelines([
            'print("Hello World !")'
        ])

    CloudRunner2(
        script_relative_path='project_0/script_local.py',
        config_relative_path='project_0/conf/config.json',
        config_generator=my_generator(),
        to_deploy=[_.path for _ in ws]
    ).run_with(cluster)
