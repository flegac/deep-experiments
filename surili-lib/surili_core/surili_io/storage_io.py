import os
import tempfile

from google.cloud import storage

from surili_core.utils import shell
from surili_core.worker import Worker
from surili_core.workspace import Workspace

GSUTIL_COPY_COMMAND = 'gsutil -m cp -r "{source_path}" "{target_path}"'


class StorageIO(object):
    def write(self, storage_path: str, local_path: str):
        shell(GSUTIL_COPY_COMMAND.format(
            source_path=local_path,
            target_path=storage_path
        )).wait()

    def read(self, storage_path: str) -> str:
        local_path = tempfile.mkdtemp()
        shell(GSUTIL_COPY_COMMAND.format(
            source_path=storage_path,
            target_path=local_path,
        )).wait()
        return local_path


class StorageExport(Worker):
    def __init__(self, storage_path: str):
        if storage_path is None or not storage_path.startswith('gs://'):
            raise ValueError("A storage path starting with 'gs://' is needed !")
        self.storage_path = storage_path

    def run(self, ws: Workspace):
        temporary_file = ws.root.archive()
        try:
            # full_storage_path = '{}/{}'.format(self.storage_path, os.path.basename(temporary_file))
            # shell(GSUTIL_COPY_COMMAND.format(source_path=temporary_file, target_path=full_storage_path)).wait()
            # time.sleep(10)

            storage_client = storage.Client()
            bucket = storage_client.get_bucket(self.storage_path)
            blob = bucket.blob(os.path.basename(temporary_file))

            blob.upload_from_filename(temporary_file)
            print('File {} uploaded to {}.'.format(
                temporary_file,
                os.path.basename(temporary_file)))

        finally:
            os.remove(temporary_file)


class StorageImport(Worker):
    def __init__(self, storage_path: str):
        if storage_path is None or not storage_path.startswith('gs://'):
            raise ValueError("A storage path starting with 'gs://' is needed !")
        self.storage_path = storage_path

    def run(self, ws: Workspace):
        ws.mkdir()
        shell(GSUTIL_COPY_COMMAND.format(
            source_path=self.storage_path,
            target_path=ws.path,
        )).wait()
        archive_name = os.path.basename(self.storage_path)
        ws.extract(ws.path_to(archive_name))
