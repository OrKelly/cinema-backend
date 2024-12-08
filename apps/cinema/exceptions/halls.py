from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.exceptions.base import InstanceAlreadyExistException


@dataclass
class HallNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Кинозал c указанными параметрами не найден"


@dataclass
class HallAlreadyExists(InstanceAlreadyExistException):
    @property
    def message(self):
        return "Кинозал с таким название уже существует"
