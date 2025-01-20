from dataclasses import dataclass

from core.exceptions import NotFoundException, ServerException


@dataclass
class FilmSessionNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Сеанс не найден"


@dataclass
class FilmSessionIncorrectDateException(ServerException):
    @property
    def message(self):
        return (
            "Сеанс не может быть назначен на это время! "
            "Фильм еще не вышел в прокате, либо уже закончил прокат"
        )


@dataclass
class FilmSessionDateConflict(ServerException):
    @property
    def message(self):
        return (
            "Сеанс конфликтует с другими сеансами! "
            "Сеанс не может начаться, пока будет идти другой фильм,"
            "либо заканчиваться позже начала другого сеанса"
        )
