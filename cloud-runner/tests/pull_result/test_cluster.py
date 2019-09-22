import os

from cloud_runner2.cloud_cluster import CloudCluster

cluster = CloudCluster(
    name='test-clusters',
    cluster_size=2,
    cluster_config=[
        '--preemptible',
        '--machine-type=n1-standard-4',
        '--image-family=ubuntu-1810',
        '--image-project=ubuntu-os-cloud',
    ]
)


def test_start():
    cluster._create_editor()

    # cluster.ssh('ls', 0)

    # cluster.stop()


def test_ssh():
    # cluster.start()

    cluster.ssh(
        commands=[
            'ls /tmp',
        ],
        instance_id=0
    ).wait()

    # cluster.stop()


def test_push_pull():
    # cluster.start()

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

    # cluster.stop()
