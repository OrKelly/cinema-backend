from dataclasses import dataclass, field
from typing import Any

from apps.notifications.services.notifications import (
    NotificationServicesFactory,
)
from apps.users.models.users import User
from apps.users.services.register import (
    BaseExistingUserValidatorService,
    BaseRegisterValidatorService,
)
from apps.users.services.users import BaseUserService
from core.enums.notifications import NotificationKindEnum
from core.enums.users import RoleKindEnum
from core.security.password import PasswordHandler


@dataclass
class RegisterUserUseCase:
    user_service: BaseUserService
    notification_service: NotificationServicesFactory(
        NotificationKindEnum.CLIENT_GREETING
    ).get_service()

    validator: BaseRegisterValidatorService

    async def execute(self, user_data: dict[str, Any]) -> User:
        await self.validator.validate(user_data)
        user = await self.user_service.create(attributes=user_data)
        await self.notification_service.send_notification(user=user)
        return user


@dataclass
class RegisterEmployeeUseCase:
    user_service: BaseUserService
    notification_service: NotificationServicesFactory(
        NotificationKindEnum.EMPLOYEE_GREETING
    ).get_service()

    existing_user_validator: BaseExistingUserValidatorService
    not_existing_user_validator: BaseRegisterValidatorService

    employee_role = RoleKindEnum.EMPLOYEE
    password: str = field(default_factory=PasswordHandler.generate_password)

    async def execute(self, user_data: dict):
        if user_id := user_data.get("user_id"):
            await self.existing_user_validator.validate(id_=user_id)
            return await self.create_employee_from_user(id_=user_id)
        return await self.create_new_employee(
            user_data=user_data["employee_data"]
        )

    async def create_employee_from_user(self, id_: int):
        user = await self.user_service.update(
            id_=id_, attributes={"role": self.employee_role}
        )
        await self.notification_service.send_notification(user=user)
        return user

    async def create_new_employee(self, user_data: dict[str, Any]):
        attributes = {"role": self.employee_role, "password": self.password}
        user_data.update(attributes)
        await self.not_existing_user_validator.validate(user_data=user_data)
        user = await self.user_service.create(attributes=user_data)
        await self.notification_service.send_notification(
            user=user, password=self.password
        )
        return user
