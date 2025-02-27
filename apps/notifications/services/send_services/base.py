from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass

from apps.notifications.models.notification import Notification
from core.loggers.base import BaseLogger


@dataclass
class BaseNotificationService(ABC):
    logger: BaseLogger

    async def notify(self, notification: Notification, kwargs: dict = None):
        self.notification = notification
        self.kwargs = kwargs

        notification_data = self._get_notification_payload()
        errors = defaultdict(list)
        await self._validate(errors)
        if errors:
            self.logger.error(
                f"Произошла ошибка при отправке уведомления. Ошибка - {errors}"
            )
        else:
            await self._notify(notification_data)

    def _get_notification_payload(self) -> dict:
        return {
            "user_id": self.notification.user_id,
            "email": self.notification.email,
            "title": self.notification.title,
            "body": self.notification.body,
        }

    @abstractmethod
    async def _validate(self, errors: dict[list]):
        """Переопределить в дочерних классах"""
        ...

    @abstractmethod
    async def _notify(self, notification_data: dict) -> None:
        """Переопредилить в дочерних классах"""
        ...
