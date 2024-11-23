from dataclasses import dataclass

from minio import Minio

from core.storages.s3.base import BaseS3Storage


@dataclass
class MinioS3Storage(BaseS3Storage):
    _client_type: Minio = Minio

    def __post_init__(self):
        super().__post_init__()

    def _ensure_bucket_exists(self):
        if not self._client.bucket_exists(self.bucket_name):
            self._client.make_bucket(self.bucket_name)

    def upload_file(self, file_path: str, object_name: str) -> None:
        self._client.fput_object(self.bucket_name, object_name, file_path)

    def download_file(self, object_name: str, file_path: str) -> None:
        self._client.fget_object(self.bucket_name, object_name, file_path)

    def delete_file(self, object_name: str) -> None:
        self._client.remove_object(self.bucket_name, object_name)
