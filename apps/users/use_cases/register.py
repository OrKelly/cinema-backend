from dataclasses import dataclass, field
from typing import Any

from apps.notifications.repositories.notification import (
    BaseNotificationRepository,
)
from apps.notifications.services.send_services.base import (
    BaseNotificationService,
)
from apps.users.models.users import User
from apps.users.services.register import (
    BaseExistingUserValidatorService,
    BaseRegisterValidatorService,
)
from apps.users.services.users import BaseUserService
from core.database import Propagation, Transactional
from core.enums.notifications import NotificationKindEnum
from core.enums.users import RoleKindEnum
from core.security.password import PasswordHandler


@dataclass
class BaseRegisterUserUseCase:
    user_service: BaseUserService
    registration_validator: BaseRegisterValidatorService
    notification_service: BaseNotificationService
    notification_repository: BaseNotificationRepository

    async def execute(self, user_data: dict[str, Any]) -> User: ...


@dataclass
class RegisterUserUseCase(BaseRegisterUserUseCase):
    async def execute(self, user_data: dict[str, Any]) -> User:
        await self.registration_validator.validate(user_data)
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


@dataclass
class RegisterEmployeeUseCase(BaseRegisterUserUseCase):
    existing_user_id_validator: BaseExistingUserValidatorService
    employee_role = RoleKindEnum.EMPLOYEE
    password: str = field(default_factory=PasswordHandler.generate_password)

    async def create_employee_from_user(self, id_: int):
        user = await self.user_service.update(
            id_=id_, attributes={"role": self.employee_role}
        )
        await self._send_notification(user)
        return user

    async def create_new_employee(self, user_data: dict[str, Any]):
        attributes = {"role": self.employee_role, "password": self.password}
        user_data.update(attributes)
        await self.registration_validator.validate(user_data=user_data)
        user = await self.user_service.create(attributes=user_data)
        await self._send_notification(user)
        return user

    async def execute(self, user_data: dict):
        if user_id := user_data.get("user_id"):
            await self.existing_user_id_validator.validate(id_=user_id)
            return await self.create_employee_from_user(id_=user_id)
        return await self.create_new_employee(
            user_data=user_data["employee_data"]
        )

    @Transactional(Propagation.REQUIRED_NEW)
    async def _send_notification(self, user: User) -> None:
        notification = await self.notification_repository.create(
            attributes=self.__get_notification_attrs(user)
        )
        await self.notification_service.notify(
            notification, kwargs=self.__get_user_kwargs(user)
        )

    def __get_user_kwargs(self, user: User) -> dict[str, Any]:
        return {
            "full_name": user.full_name,
            "email": user.email,
            "password": self.password,
        }

    def __get_notification_attrs(self, user: User) -> dict[str, Any]:
        return {
            "user_id": user.id,
            "title": "Добро пожаловать в команду!",
            "email": user.email,
            "kind": NotificationKindEnum.EMPLOYEE_GREETING,
        }
