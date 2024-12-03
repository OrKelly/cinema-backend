from dataclasses import dataclass
from typing import Any

from apps.users.exceptions.auth import CredentialsDataIsNotCorrect
from apps.users.exceptions.users import UserEmailNotFoundException
from apps.users.models.users import User
from apps.users.services.users import BaseUserService
from core.schemas.extras.auth import Token
from core.security.jwt import JWTHandler
from core.security.password import PasswordHandler


@dataclass
class BaseAuthUserUseCase:
    user_service: BaseUserService

    async def execute(
        self, credentials_data: dict[str, Any]
    ) -> User | None: ...


@dataclass
class JwtBasedAuthUserUseCase(BaseAuthUserUseCase):
    async def execute(self, credentials_data: dict[str, Any]) -> Token | None:
        user = await self._get_user(credentials_data)
        if not user:
            raise CredentialsDataIsNotCorrect()

        return await self._get_tokens(user_id=user.id)

    async def _get_user(self, credentials_data: dict[str, Any]) -> User | None:
        user = await self.user_service.get_by_email(
            email=credentials_data["email"]
        )
        if not user:
            raise UserEmailNotFoundException()
        if not PasswordHandler.verify(
            hashed_password=user.password,
            password_to_verify=credentials_data["password"],
        ):
            raise CredentialsDataIsNotCorrect()
        return user

    async def _get_tokens(self, user_id: int) -> Token:
        access_token = JWTHandler.encode({"user_id": user_id})
        refresh_token = JWTHandler.encode({"sub": "refresh_token"})
        return Token(access_token=access_token, refresh_token=refresh_token)
