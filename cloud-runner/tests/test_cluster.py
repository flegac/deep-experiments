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
    cluster.start()

    # cluster.ssh('ls', 0)

    # cluster.stop()


def test_ssh():
    cluster.ssh([
        'ls /',
    ], 0).communicate()
