from core.exceptions.base import NotFoundException, ServerException


class PlaceAlreadyTakenException(ServerException):
    @property
    def message(self):
        return "Указанное вами место уже занято!"


class OrderNotFoundException(NotFoundException):
    @property
    def message(self):
        return "Бронь не найдена!"


class UserAndEmailNotGivenException(ServerException):
    @property
    def message(self):
        return (
            "Пользователь не аутентифицирован, "
            "а так же не предоставил эл.почту!"
        )
