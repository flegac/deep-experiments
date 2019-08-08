from enum import Enum


class GpuType(Enum):
    P4 = 'nvidia-tesla-p4'
    V100 = 'nvidia-tesla-v100'
    P100 = 'nvidia-tesla-p100'
    K80 = 'nvidia-tesla-k80'


def cpu_config():
    return [
        # processing
        '--machine-type=n1-standard-4',

        # image
        '--image-family=tf-latest-cpu',
        '--image-project=deeplearning-platform-release',

        # disk
        '--boot-disk-type=pd-ssd',
        # '--boot-disk-size=50Go',
        '--scopes=storage-full,compute-rw',

        # optional
        '--preemptible',
        '--restart-on-failure',
        '--tags=http-server,https-server',
    ]


def gpu_config(gpu_type: GpuType = GpuType.K80):
    """
    https://cloud.google.com/deep-learning-vm/docs/tensorflow_start_instance
    :return:
    """
    return [
        # processing
        '--machine-type=n1-standard-8',
        '--accelerator="type={},count=1"'.format(gpu_type.value),
        '--metadata="install-nvidia-driver=True"',
        '--maintenance-policy=TERMINATE',

        # image
        '--image-family=tf-latest-gpu',
        '--image-project=deeplearning-platform-release',

        # disk
        '--boot-disk-type=pd-ssd',
        # '--boot-disk-size=50Go',
        '--scopes=storage-full',

        # optional
        '--preemptible',
        '--restart-on-failure',
        '--tags=http-server,https-server',
    ]
