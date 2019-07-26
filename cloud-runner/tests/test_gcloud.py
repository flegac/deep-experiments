from cloud_runner2.cloud import GCloud

# GCloud.login()
# GCloud.list_config()
# GCloud.list_projects()
# GCloud.select_project(project_id)

# GCloud.list_images()
# GCloud.list_instances()

project_id = GCloud.get_project_id('my-project-name')
instance_name = 'instance-runner-1'

# cloud = GCloud.create(
#     user='my-username',
#     zone='europe-west1-b',
#     instance=instance_name,
#     project_id=project_id,
#     config_path='mini_project/vm.yaml'
# )

# cloud = GCloud.connect(
#     user='my-username',
#     zone='europe-west1-b',
#     instance='runner-test-1',
#     project_id=project_id
# )
# print(cloud)

# cloud.destroy()

# cloud.ssh_connect(zone='europe-west1-b', instance=instance_name)

# cloud.copy_upload(os.path.abspath('tests'), '/tmp')

# cloud.destroy_instance(id=instance_name)

# cloud.ssh_command('echo "blabla" > /tmp/toto.txt')
