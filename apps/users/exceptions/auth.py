from dataclasses import dataclass

from core.exceptions.base import (
    InstanceAlreadyExistException,
    ServerException,
    UnauthorizedException,
)


@dataclass
class EmailAlreadyTakenException(InstanceAlreadyExistException):
    @property
    def message(self):
        return "Указанный вами email уже занят!"


@dataclass
class PasswordIncorrectException(ServerException):
    @property
    def message(self):
        return (
            "Пароль должен состоять как минимум из 8 символов, "
            "а так-же включать в себя цифру и заглавную букву"
        )


@dataclass
class CredentialsDataIsNotCorrect(UnauthorizedException):
    @property
    def message(self):
        return "Пользователь с указанными email и паролем не найден в системе"
