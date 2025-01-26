from dataclasses import dataclass

from core.exceptions import NotFoundException


@dataclass
class FilmNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Фильм не найден"
