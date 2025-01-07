from contextlib import asynccontextmanager

from core.generics import S3ClientType


@asynccontextmanager
async def remove_file_on_exception(
    storage_service: S3ClientType, file_path: str
):
    """Контекстный менеджер, удаляющий файл из S3 хранилища
    если произошло исключение

    :param storage_service: экземпляр клиента хранилища
    :param file_path: путь до файла в хранилище
    """

    try:
        yield
    except Exception as e:
        storage_service.delete_file(file_path)
        raise e
