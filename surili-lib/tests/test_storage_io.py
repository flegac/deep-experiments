from surili_core.surili_io.storage_io import StorageIO
from surili_core.workspace import Workspace

io = StorageIO()

remote_path = 'gs://flegac-test'


def test_storage_io():
    with Workspace.temporary() as ws:
        local_path = ws.create_file('toto.txt')
        io.write(remote_path, local_path)
    local_path = io.read(remote_path)
    print(local_path)
    Workspace.from_path(local_path).delete()
