from dataclasses import dataclass
from enum import Enum
from functools import wraps

from core.database import session


class Propagation(Enum):
    """
    Енам, указывающий тип транзакции

    :param REQUIRED: Если текущая транзакция уже существует,
    функция выполняется внутри этой транзакции. Если транзакции нет,
    создаётся новая.
    :param REQUIRED_NEW: Всегда создает новую транзакцию, внезависимо от того,
    есть она уже или нет
    """

    REQUIRED = "required"
    REQUIRED_NEW = "required_new"


@dataclass
class Transactional:
    """
    Класс декоратор для управления транзакциями в асинхронном режиме

    REQUIRED используется в большинстве случаев, когда ошибка в функции
    должна валить всю операцию.

    REQUIRED_NEW используется в том случае, когда ошибка не должна валить
    всю транзакцию.
    Например: формирование письма уведомления о покупке билета пользователю
    в ЛК.
    Отмена уведомления не должнаоткатить все предыдущие этапы,
    а именно: бронирование, оплату, формирование и отправку билетов.

    :param: propagation: Тип транзакции

    """

    propagation: Propagation = Propagation.REQUIRED

    def __call__(self, function):
        @wraps(function)
        async def decorator(*args, **kwargs):
            """Метод декоратора. Проверяет тип транзакции
            и на основе этого создает новую или подключает к
            существующей"""
            try:
                if self.propagation == Propagation.REQUIRED:
                    result = await self._run_required(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
                elif self.propagation == Propagation.REQUIRED_NEW:
                    result = await self._run_required_new(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
                else:
                    result = await self._run_required(
                        function=function,
                        args=args,
                        kwargs=kwargs,
                    )
            except Exception as exception:
                # если произошло исключение в ходе выполнения функции -
                # откатываем всю транзакцию и кидаем эксепшен
                await session.rollback()
                raise exception

            return result

        return decorator

    async def _run_required(self, function, args, kwargs) -> None:
        """Метод выполняет функцию в теле существующей транзакции,
        если он уже есть. Если нет - создает новую"""
        result = await function(*args, **kwargs)
        await session.commit()
        return result

    async def _run_required_new(self, function, args, kwargs) -> None:
        """Метод создает новую транзакцию для функции"""
        session.begin()
        result = await function(*args, **kwargs)
        await session.commit()
        return result
