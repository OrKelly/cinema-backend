from abc import ABC, abstractmethod
from dataclasses import dataclass

from core.config import config
from core.generics import S3ClientType


@dataclass
class BaseS3Storage(ABC):
    """
    Базовый класс для S3 хранилищ

    :param endpoint: URL хранилища
    :param access_key: ключ доступа к хранилищу
    :param secret_key: секретный ключ хранилища
    :param bucket_name: бакет, куда загружаются файлы
    :param secure: установить безопасное подключение или нет.
    :param _client_type: SDK (пакет) для создания инстанса хранилища
    """

    endpoint: str = config.S3_ENDPOINT
    access_key: str = config.S3_ACCESS_KEY
    secret_key: str = config.S3_SECRET_KEY
    bucket_name: str = config.S3_BUCKET_NAME
    _client_type: S3ClientType = S3ClientType
    secure: bool = False

    def __post_init__(self):
        try:
            self._client = self._client_type(
                self.endpoint,
                access_key=self.access_key,
                secret_key=self.secret_key,
                secure=self.secure,
            )
            if self.bucket_name:
                self._ensure_bucket_exists()
        except Exception:
            pass

    @abstractmethod
    def _ensure_bucket_exists(self):
        """Метод проверяет, существует ли указанный bucket.
        Если нет - создает
        """
        ...

    @abstractmethod
    def upload_file(self, file_path: str, object_name: str) -> None:
        """
        Метод для загрузки файла в S3 хранилище

        :param file_path: файл для загрузки (путь до него)
        :param object_name: имя файла
        :return: None
        """
        ...

    @abstractmethod
    def download_file(self, object_name: str, file_path: str) -> None:
        """
        Метод для скачивания файла из S3 хранилища

        :param file_path: путь к файлу в S3
        :param object_name: имя файла
        :return: None
        """
        ...

    @abstractmethod
    def delete_file(self, object_name: str) -> None:
        """Метод для удаления файла из S3 хранилища

        :param object_name: имя файла
        :return: None
        """
        ...
