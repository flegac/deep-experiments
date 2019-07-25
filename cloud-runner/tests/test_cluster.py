import os

from cloud_runner2.cloud_cluster import CloudCluster
from cloud_runner2.cluster_utils import cpu_config

cluster = CloudCluster(
    name='test-cluster',
    cluster_size=1,
    cluster_config=cpu_config()
)


def test_start():
    cluster.create().wait()

    cluster.ssh('ls /tmp', 0).wait()

    cluster.delete().wait()


def test_ssh():
    cluster.start()

    cluster.ssh(
        commands=[
            'ls /tmp',
        ],
        instance_id=0
    ).wait()

    cluster.stop()


def test_push_pull():
    cluster.start()

    cluster.push(
        local_path=os.getcwd(),
        remote_path='/tmp',
        instance_id=0
    ).wait()

    cluster.pull(
        local_path=os.path.join(os.getcwd(), 'pull_result'),
        remote_path='/tmp/tests',
        instance_id=0
    ).wait()

    cluster.stop()
