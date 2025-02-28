from dataclasses import dataclass, field
from typing import Any

from apps.notifications.repositories.notification import (
    BaseNotificationRepository,
)
from apps.notifications.services.send_services.base import (
    BaseNotificationService,
)
from apps.users.exceptions.auth import NoDataInFieldException
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


@dataclass
class RegisterNewEmployeeUseCase(RegisterUserUseCase):
    async def execute(self, user_data):
        return await super().execute(user_data)


@dataclass
class RegisterEmployeeUseCase:
    user_service: BaseUserService
    existing_user_validator: BaseExistingUserValidatorService
    not_existing_user_validators: BaseRegisterValidatorService
    employee_role: RoleKindEnum.EMPLOYEE
    password: str = field(default_factory=PasswordHandler.generate_password)

    async def create_employee_from_user(self, id_: int):
        return await self.user_service.update(id_, self.employee_role)

    async def create_new_employee(self, user_data: dict[str, Any]):
        # ToDo добавить отправку нотификации и пароля после успешной
        #  регистрации после введения их в систему
        attributes = {"role": self.employee_role, "password": self.password}
        user_data.update(attributes)
        return await self.user_service.create(user_data)

    async def execute(self, user_data: int):
        if user_id := user_data.get("user_id"):
            await self.existing_user_validator.validate(user_id)
            return await self.create_employee_from_user(user_id)
        if employee_data := user_data.get("employee_data"):
            await self.not_existing_user_validators.validate(employee_data)
            return await self.create_new_employee(employee_data)
        raise NoDataInFieldException
