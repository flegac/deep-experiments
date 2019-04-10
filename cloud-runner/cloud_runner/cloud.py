import os
import subprocess
from string import Template


class GCloud:

    @staticmethod
    def create(user: str, zone: str, instance: str, project_id: str, config_path: str = None):
        with open(config_path) as _:
            tpl = Template(_.read())
        config_path = os.path.abspath('/tmp/config_{}.yaml'.format(instance))
        with open(config_path, 'w') as _:
            config = tpl.substitute(
                zone=zone,
                name=instance,
                project_id=project_id
            )
            _.write(config)
        cmd = 'gcloud deployment-manager deployments create {} --config "{}"'.format(instance, config_path)
        GCloud._run(cmd)
        return GCloud(user, zone, instance, project_id)

    @staticmethod
    def connect(user: str, zone: str, instance: str, project_id: str = None, config_path: str = None):
        return GCloud(user, zone, instance, project_id)

    @staticmethod
    def login():
        GCloud._run('gcloud auth login')

    @staticmethod
    def select_project(project_id: str):
        GCloud._run('gcloud config set project {}'.format(project_id))

    @staticmethod
    def get_project_id(project_name: str):
        project_id = GCloud._run(
            'gcloud projects list --filter="name={}" --format=value(projectId)'.format(project_name))
        project_id = project_id.decode().strip()
        return project_id

    @staticmethod
    def list_config():
        GCloud._run('gcloud config list')

    @staticmethod
    def list_images():
        GCloud._run('gcloud compute images list')

    @staticmethod
    def list_projects():
        GCloud._run('gcloud projects list')

    @staticmethod
    def list_instances():
        GCloud._run('gcloud compute instances list')

    @staticmethod
    def _run(cmd):
        print(cmd)
        # return os.system(cmd)

        return subprocess.check_output(cmd, shell=True)

    def __init__(self, user: str, zone: str, instance: str, project_id: str = None):
        self.user = user
        self.zone = zone
        self.instance = instance
        self.project_id = project_id

    def destroy(self):
        cmd = 'gcloud deployment-manager deployments delete {} -q --async'.format(self.instance)
        GCloud._run(cmd)

    def ssh_connect(self):
        cmd = 'gcloud compute ssh --zone={} {}'.format(self.zone, self.instance)
        print(cmd)

    def ssh_command(self, cmd: str):
        project = '--project "{}"'.format(self.project_id) if self.project_id else ''
        cmd = 'gcloud compute ssh {} --zone={} {} --command "{}"'.format(project, self.zone, self.instance, cmd)
        GCloud._run(cmd)

    def copy_upload(self, local_path: str, remote_path: str):
        source = local_path
        target = '{}@{}:{}'.format(self.user, self.instance, remote_path)
        cmd = 'gcloud compute scp --recurse --zone={} {} {}'.format(self.zone, source, target)
        GCloud._run(cmd)

    def copy_download(self, remote_path: str, local_path: str):
        source = '{}@{}:{}'.format(self.user, self.instance, remote_path)
        target = local_path
        cmd = 'gcloud compute scp {} {}'.format(source, target)
        GCloud._run(cmd)
