from dataclasses import dataclass

from fastapi import status
from minio import Minio, S3Error
from urllib3 import HTTPResponse

from core.storages.s3.base import BaseS3Storage


@dataclass
class MinioS3Storage(BaseS3Storage):
    _client_type: Minio = Minio

    def __post_init__(self):
        super().__post_init__()

    def _ensure_bucket_exists(self):
        if not self._client.bucket_exists(self.bucket_name):
            self._client.make_bucket(self.bucket_name)

    def upload_file(self, file_path: str, object_name: str) -> HTTPResponse:
        try:
            self._client.fput_object(self.bucket_name, object_name, file_path)
            return HTTPResponse(
                status=status.HTTP_201_CREATED, body="Файл успешно загружен"
            )
        except S3Error as e:
            return HTTPResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body=f"Ошибка при загрузке файла: {e}",
            )

    def get_object(self, object_name: str) -> HTTPResponse:
        try:
            return self._client.get_object(self.bucket_name, object_name)
        except S3Error as e:
            if e.code.startswith("NoSuchKey"):
                return HTTPResponse(
                    status=status.HTTP_404_NOT_FOUND,
                    body=f"Объект {object_name} не найден",
                )
            return HTTPResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body=f"Ошибка при получении объекта: {e}",
            )

    def download_file(self, object_name: str, file_path: str) -> HTTPResponse:
        try:
            self._client.fget_object(self.bucket_name, object_name, file_path)
            return HTTPResponse(
                status=status.HTTP_200_OK, body="Файл успешно скачан"
            )
        except S3Error as e:
            return HTTPResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body=f"Ошибка при скачивании файла: {e}",
            )

    def delete_file(self, object_name: str) -> HTTPResponse:
        try:
            self._client.remove_object(self.bucket_name, object_name)
            return HTTPResponse(
                status=status.HTTP_200_OK, body="Файл успешно удален"
            )
        except S3Error as e:
            return HTTPResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body=f"Ошибка при удалении файла: {e}",
            )

    def list_objects(self, prefix: str = "") -> list | HTTPResponse:
        try:
            objects = self._client.list_objects(
                self.bucket_name, prefix=prefix
            )
            return [obj.object_name for obj in objects]
        except S3Error as e:
            return HTTPResponse(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                body=f"Ошибка при получении списка объектов: {e}",
            )
