from dataclasses import dataclass
from fastapi import status

from core.generics import ModelType


@dataclass
class ServerException(Exception):
    """
    Базовый класс эксепшенов. Для создания своего собственного отнаследоваться от него
    и переопределить.

    :param code: HTTP статус код, возвращаемый в респонсе
    :param error_code: код самой ошибки. Нужен для более гибкого логирования и сбора метрик в будущем.
    :param message: сообщение ошибки
    """
    code: status.HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    error_code: status.HTTP_400_BAD_REQUEST = status.HTTP_400_BAD_REQUEST
    message: str = "Произошла непредвиденная ошибка во время работы приложения"


@dataclass
class NotFoundException(ServerException):
    code: status.HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND
    error_code: status.HTTP_404_NOT_FOUND = status.HTTP_404_NOT_FOUND


@dataclass
class ForbiddenException(ServerException):
    code: status.HTTP_403_FORBIDDEN = status.HTTP_403_FORBIDDEN
    error_code: status.HTTP_403_FORBIDDEN = status.HTTP_403_FORBIDDEN


@dataclass
class UnauthorizedException(ServerException):
    code: status.HTTP_401_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
    error_code: status.HTTP_401_UNAUTHORIZED = status.HTTP_401_UNAUTHORIZED
