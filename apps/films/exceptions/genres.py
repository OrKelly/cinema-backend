from dataclasses import dataclass

from core.exceptions import NotFoundException


@dataclass
class GenreNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Жанр не найден"
