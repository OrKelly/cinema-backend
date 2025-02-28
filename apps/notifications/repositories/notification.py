from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from apps.notifications.models.notification import Notification
from core.repositories.base import BaseORMRepository


@dataclass
class BaseNotificationRepository(ABC):
    @abstractmethod
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Notification | None: ...


@dataclass
class ORMNotificationRepository(
    BaseNotificationRepository, BaseORMRepository[Notification]
):
    async def create(
        self, attributes: dict[str, Any] = None
    ) -> Notification | None:
        return await super(BaseNotificationRepository, self).create(
            attributes=attributes
        )
