from dataclasses import dataclass
from typing import Any

from apps.users.models.users import User
from apps.users.services.register import BaseRegisterValidatorService
from apps.users.services.users import BaseUserService
from core.enums.users import RoleKindEnum


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
class RegisterEmployeeUseCase(RegisterUserUseCase):
    async def execute(self, user_data: dict[str, Any]):
        user_data['role'] = RoleKindEnum.EMPLOYEE
        return await super().execute(user_data)
