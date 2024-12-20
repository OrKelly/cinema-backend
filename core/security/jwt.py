from dataclasses import dataclass
from datetime import datetime, timedelta

from fastapi import status
from jose import ExpiredSignatureError, JWTError, jwt

from core.config import config
from core.exceptions import ServerException


class JWTDecodeError(JWTError, ServerException):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Invalid token"


class JWTExpiredError(JWTError, ServerException):
    code = status.HTTP_401_UNAUTHORIZED
    message = "Token expired"


@dataclass
class JWTHandler:
    secret_key: config.SECRET_KEY = config.SECRET_KEY
    algorythm: config.JWT_ALGORYTHM = config.JWT_ALGORYTHM
    expire_minutes: config.JWT_EXPIRE_MINUTES = config.JWT_EXPIRE_MINUTES

    @classmethod
    def encode(cls, payload: dict) -> str:
        expire = datetime.now() + timedelta(minutes=cls.expire_minutes)
        payload.update({"exp": expire})
        return jwt.encode(payload, cls.secret_key, algorithm=cls.algorythm)

    @classmethod
    def decode(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token, cls.secret_key, algorithms=[cls.algorythm]
            )
        except ExpiredSignatureError as exception:
            raise JWTExpiredError() from exception
        except JWTError as exception:
            raise JWTDecodeError() from exception

    @classmethod
    def decode_expired(cls, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[cls.algorythm],
                options={"verify_exp": False},
            )
        except JWTError as exception:
            raise JWTDecodeError() from exception
