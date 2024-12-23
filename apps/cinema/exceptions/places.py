from dataclasses import dataclass

from core.exceptions import NotFoundException
from core.exceptions.base import InstanceAlreadyExistException


@dataclass
class PlaceNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Место с указанными параметрами не найдено"


@dataclass
class PlaceAlreadyExistsException(InstanceAlreadyExistException):
    @property
    def message(self):
        return "Место такого ряда, с таким номером уже существует"
