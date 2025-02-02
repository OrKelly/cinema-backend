from dataclasses import dataclass, field
from typing import Any, Dict

from apps.users.models.users import User
from apps.users.services.register import (
    BaseRegisterValidatorService,
    BaseExistingUserValidatorService,
    BaseEmployeeValidatorService,
)
from apps.users.services.users import BaseUserService
from core.enums.users import RoleKindEnum
from core.security.password import PasswordHandler
from apps.users.exceptions.auth import NoDataInFieldException


@dataclass
class BaseRegisterUserUseCase:
    user_service: BaseUserService
    validator: BaseRegisterValidatorService

    async def execute(self, user_data: dict[str, Any]) -> User: ...


@dataclass
class RegisterUserUseCase(BaseRegisterUserUseCase):
    async def execute(self, user_data: dict[str, Any]) -> User:
        # ToDo добавить отправку нотификации после успешной
        #  регистрации после введения их в систему
        await self.validator.validate(user_data)
        return await self.user_service.create(attributes=user_data)


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
