from dataclasses import dataclass

from core.exceptions import NotFoundException


@dataclass
class UserNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Пользователь не найден"


@dataclass
class UserEmailNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Пользователь с указанным email не найден!"
