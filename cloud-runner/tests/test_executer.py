from cloud_runner.cluster.google_cluster import GoogleCluster
from cloud_runner.cluster.google_utils import cpu_config
from cloud_runner.cluster.local_cluster import LocalCluster
from cloud_runner.script_runner import ScriptRunner
from surili_core.workspace import Workspace

google_cluster = GoogleCluster(
    name='test-cluster',
    cluster_size=2,
    cluster_config=cpu_config()
)
local_cluster = LocalCluster(
    cluster_size=1,
    remote_workspace=Workspace.temporary().path
)


def test_executer():
    cluster = google_cluster

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

    ScriptRunner(
        script_relative_path='project_0/script_local.py',
        config_relative_path='project_0/conf/config.json',
        configs=[
            {
                'a': 'aaaaa',
                'b': 'bbbbb'
            } for _ in range(cluster.cluster_size())
        ],
        to_deploy=[_.path for _ in ws]
    ).run_with(cluster)
