from dataclasses import dataclass
from typing import Any

from apps.notifications.repositories.notification import (
    BaseNotificationRepository,
)
from apps.notifications.services.send_services.base import (
    BaseNotificationService,
)
from apps.users.models.users import User
from apps.users.services.register import BaseRegisterValidatorService
from apps.users.services.users import BaseUserService
from core.database import Propagation, Transactional
from core.enums.notifications import NotificationKindEnum


@dataclass
class BaseRegisterUserUseCase:
    user_service: BaseUserService
    validator: BaseRegisterValidatorService
    notification_service: BaseNotificationService
    notification_repository: BaseNotificationRepository

    async def execute(self, user_data: dict[str, Any]) -> User: ...


@dataclass
class RegisterUserUseCase(BaseRegisterUserUseCase):
    async def execute(self, user_data: dict[str, Any]) -> User:
        await self.validator.validate(user_data)
        user = await self.user_service.create(attributes=user_data)
        await self._send_notification(user)
        return user

    @Transactional(Propagation.REQUIRED_NEW)
    async def _send_notification(self, user: User) -> None:
        notification = await self.notification_repository.create(
            attributes=self.__get_notification_attrs(user)
        )
        await self.notification_service.notify(
            notification, kwargs=self.__get_user_kwargs(user)
        )

    def __get_user_kwargs(self, user: User) -> dict[str, Any]:
        return {"full_name": user.full_name}

    def __get_notification_attrs(self, user: User) -> dict[str, Any]:
        return {
            "user_id": user.id,
            "title": "Добро пожаловать!",
            "email": user.email,
            "kind": NotificationKindEnum.CLIENT_GREETING,
        }
