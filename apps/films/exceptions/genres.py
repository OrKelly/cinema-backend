from dataclasses import dataclass

from core.exceptions import NotFoundException


@dataclass
class GenreNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Жанр не найден"


class GenreExistValidateException(NotFoundException):

    def __init__(self, val):
        self.val = val

    @property
    def message(self):
        if len(self.val) > 1:
            return f"Жанры {self.val} не найдены"
        return f"Жанр {self.val} не найден"
