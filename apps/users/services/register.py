import re
from abc import ABC, abstractmethod
from dataclasses import dataclass

from apps.users.exceptions.auth import (
    EmailAlreadyTakenException,
    PasswordIncorrectException,
)
from apps.users.services.users import BaseUserService


@dataclass
class BaseRegisterValidatorService(ABC):
    @abstractmethod
    async def validate(self, user_data: dict[str, any]) -> None: ...


@dataclass
class UniqueEmailValidatorService(BaseRegisterValidatorService):
    user_service: BaseUserService

    async def validate(self, user_data: dict[str, any]) -> None:
        user = await self.user_service.get_by_email(email=user_data["email"])
        if user:
            raise EmailAlreadyTakenException


@dataclass
class PasswordIncorrectValidatorService(BaseRegisterValidatorService):
    password_regex: re.Pattern = r"^(?=.*\d)(?=.*[A-Z]).{8,}$"

    async def validate(self, user_data: dict[str, any]) -> None:
        if not re.match(self.password_regex, user_data["password"]):
            raise PasswordIncorrectException


@dataclass
class ComposedRegisterValidatorService(BaseRegisterValidatorService):
    validators: list[BaseRegisterValidatorService]

    async def validate(self, user_data: dict[str, any]) -> None:
        for validator in self.validators:
            await validator.validate(user_data)
