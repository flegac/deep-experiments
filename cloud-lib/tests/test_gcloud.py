from cloud_lib.cloud import GCloud

cloud = GCloud(user='florent',
               zone='europe-west1-b',
               instance='instance-1')

# cloud.login()
# cloud.select_project('flegac-deep')

# cloud.compute_images_list()
# cloud.ssh_connect(zone='europe-west1-b', instance='instance-1')


# cloud.copy_upload('/home/flegac/Documents/python/', '/home/florent/')

# cloud.create_instance(id='test-instance', config_path='/resources/vm.yaml')
# cloud.destroy_instance(id='test-instance')
# cloud.destroy_instance(id='quickstart-deployment')

cloud.ssh_command('cd /home/florent && echo "blabla" > toto.txt')