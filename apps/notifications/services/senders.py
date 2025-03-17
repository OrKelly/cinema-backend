from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, TypeVar

from apps.mail_service.base import BaseMailClient
from apps.notifications.repositories.notification import (
    BaseNotificationRepository,
)
from apps.users.models import User
from core.database import Propagation, Transactional
from core.enums.notifications import NotificationKindEnum

HTMLTemplate = TypeVar("HTMLTemplate")
RenderedTemplate = TypeVar("RenderedTemplate")

# TODO переработать шаблоны уведомлений
#  (работа стилей, логотип, улучшить тексты приветствий)


@dataclass
class EmailNotificationService(ABC):
    mail_service: BaseMailClient
    notification_repository: BaseNotificationRepository

    @Transactional(Propagation.REQUIRED_NEW)
    @abstractmethod
    async def send_notification(self, user: User) -> None: ...

    @abstractmethod
    def get_notification_attrs(self, user: User) -> dict[str, Any]: ...


class ClientGreetingNotificationService(EmailNotificationService):
    template = "client_greeting.html"

    @Transactional(Propagation.REQUIRED_NEW)
    async def send_notification(self, user: User) -> None:
        kwargs = {
            "full_name": user.full_name,
        }
        notification = await self.notification_repository.create(
            attributes=self.get_notification_attrs(user)
        )
        await self.mail_service.notify(
            notification=notification, template=self.template, kwargs=kwargs
        )

    def get_notification_attrs(self, user: User) -> dict[str, Any]:
        return {
            "user_id": user.id,
            "title": "Добро пожаловать!",
            "email": user.email,
            "kind": NotificationKindEnum.CLIENT_GREETING,
        }


class EmployeeGreetingNotificationService(EmailNotificationService):
    template = "employee_greeting.html"

    @Transactional(Propagation.REQUIRED_NEW)
    async def send_notification(
        self, user: User, password: str = None
    ) -> None:
        kwargs = {
            "full_name": user.full_name,
            "email": user.email,
            "password": password,
        }
        notification = await self.notification_repository.create(
            attributes=self.get_notification_attrs(user)
        )
        await self.mail_service.notify(
            notification=notification, template=self.template, kwargs=kwargs
        )

    def get_notification_attrs(self, user: User) -> dict[str, Any]:
        return {
            "user_id": user.id,
            "title": "Добро пожаловать в команду!",
            "email": user.email,
            "kind": NotificationKindEnum.EMPLOYEE_GREETING,
        }


@dataclass
class NotificationServicesFactory:
    notification_kind: NotificationKindEnum
    notification_services = {
        NotificationKindEnum.CLIENT_GREETING: ClientGreetingNotificationService,  # noqa: E501
        NotificationKindEnum.EMPLOYEE_GREETING: EmployeeGreetingNotificationService,  # noqa: E501
    }

    def get_service(self):
        return self.notification_services.get(self.notification_kind)
