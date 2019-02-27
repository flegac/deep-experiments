import shlex
import subprocess


class GCloud:
    def __init__(self, user: str, zone: str, instance: str):
        self.user = user
        self.zone = zone
        self.instance = instance

    def login(self):
        self._run('gcloud auth login')

    def select_project(self, project_id: str):
        self._run('gcloud config set project {}'.format(project_id))

    def compute_images_list(self):
        self._run('gcloud compute images list')

    def ssh_connect(self):
        cmd = 'gcloud compute ssh --zone={} {}'.format(self.zone, self.instance)
        print(cmd)

    def ssh_command(self, cmd: str):
        cmd = "gcloud compute ssh --zone={} {} --command '{}'".format(self.zone, self.instance, cmd)
        self._run(cmd)

    def copy_upload(self, local_path: str, remote_path: str):
        source = local_path
        target = '{}@{}:{}'.format(self.user, self.instance, remote_path)
        cmd = 'gcloud compute scp {} {}'.format(source, target)
        self._run(cmd)

    def copy_download(self, remote_path: str, local_path: str):
        source = '{}@{}:{}'.format(self.user, self.instance, remote_path)
        target = local_path
        cmd = 'gcloud compute scp {} {}'.format(source, target)
        self._run(cmd)

    def create_instance(self, id: str, config_path: str):
        cmd = 'gcloud deployment-manager deployments create {} --config {}'.format(id, config_path)
        self._run(cmd)

    def destroy_instance(self, id: str):
        cmd = 'gcloud deployment-manager deployments delete {} -y'.format(id)
        self._run(cmd)

    def _run(self, cmd):
        print(cmd)
        return subprocess.run(shlex.split(cmd))
